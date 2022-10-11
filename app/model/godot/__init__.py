from utils.db.helper import MgDB
from config.db import GodotDB as mg
from config.local import timestamp
import pandas as pd



class GodotM:
    def __init__(self,collection) -> None:
        self.timestamp = timestamp()
        self.col = MgDB(host=mg.HOST,port=mg.PORT,username=mg.USER,password=mg.PASSWORD,database=mg.DB,collection=collection)

    def update(self,where,update,*args,**kwargs):
        rst = self.col.update_many(where,update,upsert=True,*args,**kwargs)
        return rst.modified_count


    def update_one(self,where,update,*args,**kwargs):
        rst = self.col.update_one(where,update,upsert=True,*args,**kwargs)
        return rst.modified_count

    def select(self,where,*args,**kwargs):
        df1 = pd.DataFrame([i for i in self.col.find_many(where)])
        return df1

    def first(self,where,*args,**kwargs):
        return pd.Series(self.col.find_one(where))

    def save(self,doc):
        if '_id' in doc:    
            return self.col.replace_one({'_id': doc['_id']}, doc)
        else:
            return self.col.insert_one(doc)

    def insert_one(self,*args,**kwargs):
        return self.col.insert_one(*args,**kwargs)




