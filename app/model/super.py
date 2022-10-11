from .db.pgsql import CRUD,RedisDB,PgDB
from utils.middleware import Rsp,G
from config import Session,CacheDF,BliDB
from config.local import localtime


class SuperM(CRUD):
    def __init__(self,table):
        CRUD.__init__(self,schema="super",table=table)
        self.now = localtime()
        self.uid = 0
        self.con=PgDB(host=BliDB.HOST,port=BliDB.PORT,user=BliDB.DBUSER,password=BliDB.DBPWD,database=BliDB.DBNAME)
        self.session = RedisDB(host=Session.HOST,port=Session.PORT,db=Session.DB)
        self.CacheDF = RedisDB(host=CacheDF.HOST,port=CacheDF.PORT,db=CacheDF.DB)
    
        self.gu = G.get_uid()
        if "super" in self.gu:
            self.uid = self.gu['super']
            alias = "dp:{}".format(self.uid)
            if self.session.exists(alias) == 0:
                Rsp.no_power(msg='账号已注销')

