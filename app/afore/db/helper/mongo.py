import pymongo

class MgDB():
    def __init__(self,host,port,username,password,database,collection=None):
        uri = f'mongodb://{username}:{password}@{host}:{port}'
        client = pymongo.MongoClient(uri)
        self._db = client[database]
        if collection:
            self._col = self._db[collection]

    def get_collection(self,collection):
        self._col = self._db[collection]
        return self

    def insert_one(self,*args,**kwargs):
        rst = self._col.insert_one(*args,**kwargs)
        return rst.inserted_id

    def insert_many(self,*args,**kwargs):
        rst = self._col.insert_many(*args,**kwargs)
        return rst.inserted_ids

    def find_one(self,*args,**kwargs):
        rst = self._col.find_one(*args,**kwargs)
        return rst

    def find_many(self,*args,**kwargs):
        rst = self._col.find(*args,**kwargs)
        return rst

    def update_one(self,*args,**kwargs):
        rst = self._col.update_one(*args,**kwargs)
        return rst

    def update_many(self,*args,**kwargs):
        rst = self._col.update_many(*args,**kwargs)
        return rst

    def delete_one(self,*args,**kwargs):
        rst = self._col.delete_one(*args,**kwargs)
        return rst

    def delete_many(self,*args,**kwargs):
        rst = self._col.delete_many(*args,**kwargs)
        return rst

    def replace_one(self,*args,**kwargs):
        return self._col.replace_one(*args,**kwargs)








if __name__ == '__main__':
    db = MgDB(host='118.193.46.124',port='27017',username='root',password='aak123456',database='DB_GODOT')
    mycol = db.get_collection('roles')

    for i in mycol.find_many():
        print(i)


    