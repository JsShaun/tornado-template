from .db.pgsql import CRUD,PgDB
from utils.middleware import G
from utils import mutate_dict
from utils.middleware import Rsp
from config import BliDB
from config.local import localtime
from config.file import PATTERN



class PublicM(CRUD):
    '''数据权限代码在这里书写'''
    def __init__(self,table):
        CRUD.__init__(self,schema="public",table=table)
        self.now = localtime()
        self.uid, self.user = 0, {}
        self.con=PgDB(host=BliDB.HOST,port=BliDB.PORT,user=BliDB.DBUSER,password=BliDB.DBPWD,database=BliDB.DBNAME)
        self.gu = G.get_uid()
        for k,v in self.gu.items():
            self.uid = v
            self.user  = "{}::{}".format(k,v)

    @staticmethod
    def shield(w):
        '屏蔽敏感词语'
        if isinstance(w, str):
            w = PATTERN.sub(r'*',w)
        return w
            
    def insert(self, **kwargs) -> id:
        mutate_dict(self.shield,kwargs) # 所有插入为字符的过滤敏感词
        if "super" not in self.gu:
            Rsp.no_power()
        return super().insert(**kwargs)

    def update(self, id, *idList, **kwargs):
        if "super" not in self.gu:
            Rsp.no_power()
        return super().update(id, *idList, **kwargs)

    def delete(self, id, *idList, params={}) -> int:
        if "super" not in self.gu:
            Rsp.no_power()
        return super().delete(id, *idList, params=params)


        