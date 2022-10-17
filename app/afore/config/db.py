from afore.db.helper import PgDB
from afore.cache.helper import RedisDB
from afore.db.helper import MgDB


class BliDB:
    HOST = "127.0.0.1"
    PORT = 5432
    DBUSER = "postgres"
    DBPWD = "123456"
    DBNAME = "postgres"
    
    @classmethod
    def dbcon(cls):
        return PgDB(host=cls.HOST,port=cls.PORT,user=cls.DBUSER,password=cls.DBPWD,database=cls.DBNAME)


class Session:
    HOST = "127.0.0.1"
    PORT = 6379
    DB = 0

    @classmethod
    def dbcon(cls):
        return RedisDB(host=cls.HOST,port=cls.PORT,db=cls.DB)


class CacheDF:
    HOST = "127.0.0.1"
    PORT = 6379
    DB = 1

    @classmethod
    def dbcon(cls):
        return RedisDB(host=cls.HOST,port=cls.PORT,db=cls.DB)

class GodotDB:
    HOST = "127.0.0.1"
    PORT = 27017
    USER = "root"
    PASSWORD = ""
    DB = "Godot"

    @classmethod
    def gtcol(cls,collection):
        return MgDB(host=cls.HOST,port=cls.PORT,username=cls.USER,password=cls.PASSWORD,database=cls.DB,collection=collection)

