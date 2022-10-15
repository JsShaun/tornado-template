from .helper import PgDB
import pandas as pd
from datetime import datetime


class CRUD(object):
    '''
    PgSQL增删改查帮助类
    参数:
        session <- 会话缓存；
        con <- 数据库连接；
        uid <- 认证用户ID。
    '''
    def __init__(self,schema,table):
        self.now = datetime.now()
        self.uid:int=None
        self.con:PgDB=None
        self.schema = schema
        self.table = table
       

    def insert(self, **kwargs) -> id:
        '''插入数据
        参数：
            kwargs {column: value ...}
        返回：
            lastrowid 新建ID
        '''
        kwSeries = pd.Series(kwargs)
        kwSeries['creator'] = self.uid
        kwSeries['create_time'] = self.now
        kwSeries['operator'] = self.uid
        kwSeries['operat_time'] = self.now
        kwSeries['is_delete'] = False
        
        columnSql, valueSql = "", ""        
        for i in kwSeries.keys():
            columnSql += '"{}",'.format(i)
            valueSql += '%({})s,'.format(i)
        
        sqltext = '''
        INSERT INTO "{schema}"."{table}"({columns})
        VALUES ({values}) RETURNING id
        '''.format(schema=self.schema,table=self.table, columns=columnSql[:-1], values=valueSql[:-1])
        return self.con.insert(sqltext, **kwSeries.to_dict())

    def delete(self, id, *idList, params={}) -> int:
        '''删除数据
        参数：
            idList <- 要删除数据的Id列表
        返回：
            rowcount
        '''
        pSeries = pd.Series(params)
        if idList:
            idList = list(idList)
            idList.append(id)
            pSeries['id'] = idList
        elif id:
            pSeries['id'] = id
        whereSql = ''
        for i,v in pSeries.items():
            if isinstance(v,tuple):
                whereSql += ' AND "{0}" IN %({0})s'.format(i)
            elif isinstance(v,list):
                whereSql += ' AND "{0}" IN %({0})s'.format(i)
                pSeries[i] = tuple(v)
            else:
                whereSql += ' AND "{0}" = %({0})s'.format(i)

        sqltext = """
        UPDATE "{schema}"."{table}"
        SET "is_delete" = TRUE, "operator" = {operator}, "operat_time" = '{operat_time}'
        WHERE 1+1=2 {whereSql}
        """.format(schema=self.schema, table=self.table, operator=self.uid, operat_time=self.now,whereSql=whereSql)
        return self.con.modify(sqltext,**pSeries.to_dict())


    def update(self, id, *idList, **kwargs):
        '''修改指定ID数据
        参数：
            kwargs {column: value ...}
        返回：
            rowcount
        '''
        if idList:
            idList = list(idList)
            idList.append(id)
            id = tuple(idList)
        elif id:
            id = (id,)
        else:
            return

        setSql = " "
        kwSeries = pd.Series(kwargs)
        for key, value in kwSeries.items():
            if value is not None:
                setSql += """ "{key}" = %({key})s ,""".format(key=key)
        else:
            setSql=setSql[:-1]

        
        sqltext = """
        UPDATE "{schema}"."{table}" 
        SET {setSql}, "operator" = {operator}, "operat_time" = '{operat_time}'
        WHERE "id" IN %(id)s
        """.format(schema=self.schema,table=self.table, setSql=setSql, operator=self.uid, operat_time=self.now)
        return self.con.modify(sqltext, id=id, **kwSeries.to_dict())
    
    def echo(self,id=0,params={}) -> pd.Series:
        '''回显：
            如果ID!=0, 查询ID对应数据回显
            如果ID=0, 获取params对应条件获取数据
        返回TOP1数据
        '''
        
        pSeries = pd.Series(params)
        if id:
            pSeries['id'] = int(id)
        whereSql = ''
        for i,v in pSeries.items():
            if isinstance(v,(tuple,list)):
                whereSql += ' AND "{0}" IN %({0})s'.format(i)
            else:
                whereSql += ' AND "{0}" = %({0})s'.format(i)

        sqltext = """
        SELECT * FROM "{schema}"."{table}"
        WHERE is_delete IS FALSE {whereSql}
        """.format(schema=self.schema,table=self.table,whereSql=whereSql)
        for _,ss in self.con.pandas(sql=sqltext,params=pSeries.to_dict()).iterrows():
            if 'is_delete' in ss.keys():
                ss.pop('is_delete')
            return ss
        else:
            return pd.Series()
    
    def exist(self, params={}) -> int:
        '''数据是否存在
        参数：
            kwargs {column: value ...}
        返回：
            id
        '''
        pSeries = pd.Series(params)
        whereSql = ''
        for i,v in pSeries.items():
            if isinstance(v,(tuple,list)):
                whereSql += ' AND "{0}" IN %({0})s'.format(i)
            else:
                whereSql += ' AND "{0}" = %({0})s'.format(i)

        sqltext = """
        SELECT id FROM "{schema}"."{table}" WHERE "is_delete" IS FALSE {whereSql} 
        """.format(schema=self.schema,table=self.table,whereSql=whereSql)
        for _,ss in self.con.pandas(sql=sqltext,params=pSeries.to_dict()).iterrows():
            return ss['id']
        else:
            return 0

    
    def first(self,sqltext:str,params={}) -> pd.Series:
        '''sql查询：
        参数：
            sqltext：
                执行sqltext语句，sqltext自带 %(params)s 占位符。
            params：
                字典数据key-values
        
        返回查询的第一条数据
        '''
        
        for _,ss in self.con.pandas(sql=sqltext,params=params).iterrows():
            if 'is_delete' in ss.keys():
                ss.pop('is_delete')
            return ss
        else:
            return pd.Series()
    
    def select(self,sqltext:str,params={}) -> dict:
        
        '''查询数据表
        参数：
            sqltext：
                执行sqltext语句，sqltext自带 %(params)s 占位符。
            params：
                字典数据key-values
        '''
        pSeries = pd.Series(params)
        size = int(pSeries.pop('size')) if 'size' in pSeries.index else 10
        offset = size*(int(pSeries.pop('offset'))-1) if 'offset' in pSeries.index else 0
        sqltext = sqltext.replace('SELECT','SELECT COUNT(1)OVER()AS _total,',1)
        sqltext += ' LIMIT {:d} OFFSET {:d}'.format(size,offset)

        data = {}
        self.dataFrame  = pd.DataFrame()
        for df in self.con.pandas(sql=sqltext,params=pSeries.to_dict(),chunksize=size):
            self.dataFrame:pd.DataFrame = df
            data['total'] = df['_total'][0]
            data['detail'] = df.drop(columns='_total').to_dict('records')
            return data

        else:
            data['total'] = 0
            data['detail'] = pd.DataFrame().to_dict('records')
            return data

    def data_frame(self,sqltext,params={}):
        '''返回数据集'''
        return self.con.pandas(sql=sqltext,params=params)

    def __del__(self):
        del self.uid
        del self.schema
        del self.table
  


        






   
            


        
    
        
        
        
