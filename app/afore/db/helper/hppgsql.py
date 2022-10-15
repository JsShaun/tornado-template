import numpy as np
import pandas as pd
from psycopg2 import pool
from psycopg2.extensions import register_adapter, AsIs


def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)
def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)
register_adapter(np.float64, addapt_numpy_float64)
register_adapter(np.int64, addapt_numpy_int64)


class PgDB():
    '''PostgreSQL连接
    '''
    PGPOOL:pool.SimpleConnectionPool=None
    def __init__(self,host,port,user,password,database):
        '''简单pgsql链接池管理'''
        if not self.__class__.PGPOOL:
            self.__class__.PGPOOL = pool.SimpleConnectionPool(minconn=1, maxconn=150, user=user, password=password, host=host, port=port, database=database)
 
    
    @property
    def ping(self)->str:
        """预计返回`pong`"""
        while not self.__class__.PGPOOL.closed:
            try:
                conn = self.__class__.PGPOOL.getconn()
                with conn.cursor() as cur:
                    cur.execute("SELECT 'pong'")
                    for i in cur.fetchone():
                        return i
            except pool.PoolError:
                self.__class__.PGPOOL.closeall()
            finally:
                self.__class__.PGPOOL.putconn(conn)
            
    def insert(self,sql,*args,**kwargs):
        if self.ping != "pong": raise Exception("pgsql ping is fail !")
        '''
        执行SQL语句,返回插入ID
        参数类型：
            列表：(param1, param2, param3, param4 ...)
            字典：(param1=value1, param2=value2, param3=value3, param4=value4 ...)
            无参数
        返回 (+RETURNING id)：lastrowid
        '''
        try:
            conn = self.__class__.PGPOOL.getconn()
            with conn.cursor() as cur:
                if args:
                    cur.execute(sql,args)
                elif kwargs:
                    cur.execute(sql,kwargs)
                else:
                    cur.execute(sql)
                conn.commit()
                return cur.fetchone()
        except: raise
        finally: self.__class__.PGPOOL.putconn(conn)

    def modify(self,sql,*args,**kwargs) -> int:
        if self.ping != "pong": raise Exception("pgsql ping is fail !")
        '''
        执行SQL语句,错误则回滚
        参数类型：
            列表：params is list
            字典：params is dict
            无参数 params is None
        返回：影响行数
        '''
        try:
            conn = self.__class__.PGPOOL.getconn()
            with conn.cursor() as cur:
                if args:
                    cur.execute(sql,args)
                elif kwargs:
                    cur.execute(sql,kwargs)
                else:
                    cur.execute(sql)
                conn.commit()
                return cur.rowcount
        except: raise
        finally: self.__class__.PGPOOL.putconn(conn)



    def pandas(self,sql,params={},*args,**kwargs) -> pd.DataFrame:
        if self.ping != "pong": raise Exception("pgsql ping is fail !")
        '''
        pandas查询方式，返回DataFrame格式数据
        '''
        try:
            conn = self.__class__.PGPOOL.getconn()
            return pd.read_sql_query(sql=sql,con=conn,params=params, *args,**kwargs) 
        except: raise
        finally: self.__class__.PGPOOL.putconn(conn)

 

import time
if __name__ == '__main__':

    ss1 = pd.Series([1])

    hp = PgDB(host='118.193.46.124',port=5432,user='postgres',password='cbyzYs3QO@u8W2U!&7p',database='postgres')
    sql = """
    SELECT *
    FROM super."user"
    """
    while 1:
        try:
            time.sleep(2)
            rsp = hp.pandas(sql=sql)
            
            print(rsp.to_dict('records'))
        except Exception as e:
            print("000000000000000000000000000",str(e))

    # for i in rsp:

    #     print(i)
    
    del hp


        
        
        
        

