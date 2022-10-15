from  afore.db import CRUD
from afore.middleware import Rsp
from afore.utils import G
from afore.config import Session,CacheDF,BliDB
from afore.config import localtime


class SuperM(CRUD):
    def __init__(self,table):
        CRUD.__init__(self,schema="super",table=table)
        self.now = localtime()
        self.uid = 0
        self.con=BliDB.dbcon()
        self.session = Session.dbcon()
        self.CacheDF = CacheDF.dbcon()
    
        self.gu = G.get_uid()
        if "super" in self.gu:
            self.uid = self.gu['super']
            alias = "dp:{}".format(self.uid)
            if self.session.exists(alias) == 0:
                Rsp.no_power(msg='账号已注销')

