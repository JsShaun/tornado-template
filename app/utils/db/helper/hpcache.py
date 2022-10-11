import redis
import pandas as pd
from io import BytesIO



class RedisDB():
    '''Redis缓存帮助类'''

    __pool:redis.ConnectionPool = None
    def __init__(self,host,port,db):
        '''初始化连接'''
        if not self.__pool:
            self.__class__.__pool = redis.ConnectionPool(host=host, port=port, db=db)
        self.__get_conn()
        

    def __get_conn(self):
        self.link = redis.Redis(connection_pool=self.__pool)


    def store_str(self, alias:str, local_str:str, ex:pd.Timedelta, *args, **kwargs) -> bool:
        '''存储Str数据类型的缓存'''
        return self.link.set(name=alias, value=local_str, ex=ex, *args, **kwargs)

    def load_str(self, alias:str) -> str:
        '''加载Str数据类型的缓存'''
        return self.link.get(name=alias)

    def store_series(self, alias:str, local_series:pd.Series, ex:pd.Timedelta, *args, **kwargs) -> bool:
        '''存储Series数据类型的缓存'''
        with BytesIO() as f:
            local_series.to_pickle(f)
            return self.link.set(name=alias, value=f.getvalue(), ex=ex, *args, **kwargs)

    def load_series(self, alias:str) -> pd.Series:
        '''加载Series数据类型的缓存'''
        pickle_series = self.link.get(name=alias)
        with BytesIO(pickle_series) as f:
            return pd.read_pickle(f)

    def store_dataframe(self, alias:str, local_dataframe:pd.DataFrame,ex:pd.Timedelta,*args, **kwargs) -> bool:
        '''存储DataFrame数据类型的缓存'''
        with BytesIO() as f:
            local_dataframe.to_pickle(f)
            return self.link.set(name=alias, value=f.getvalue(), ex=ex, *args, **kwargs)

    def load_dataframe(self, alias:str) -> pd.DataFrame:
        '''加载DataFrame数据类型的缓存'''
        pickle_dataframe = self.link.get(name=alias)
        with BytesIO(pickle_dataframe) as f:
            return pd.read_pickle(f)

    def delete(self, *alias:str) -> int:
        '''删除别名对于缓存'''
        return self.link.delete(*alias)


    def exists(self,*alias:str) -> int:
        '''返回存在的名称数'''
        return self.link.exists(*alias)
            
    def __del__(self):
        '''自动释放Redis连接'''
        if self.link:
            self.link.close()


if __name__ == '__main__':
    HOST = "192.168.10.235"
    PORT = 6379
    DB = 1
    hp = Helper(host=HOST,port=PORT,db=DB)
    a = hp.exists('dp:1')
    print(a)