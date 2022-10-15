from afore.db.pgsql import CRUD
from afore.utils import G
from afore.utils import filter_word,mutate_dict
from afore.middleware import Rsp
from afore.config import BliDB
from afore.config import localtime




class PublicM(CRUD):
    '''数据权限代码在这里书写'''
    def __init__(self,table):
        CRUD.__init__(self,schema="public",table=table)
        self.now = localtime()
        self.uid, self.user = 0, {}
        self.con=BliDB.dbcon()
        self.gu = G.get_uid()
        for k,v in self.gu.items():
            self.uid = v
            self.user  = "{}::{}".format(k,v)
            
    def insert(self, **kwargs) -> id:
        mutate_dict(filter_word,kwargs) # 所有插入为字符的过滤敏感词
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


        