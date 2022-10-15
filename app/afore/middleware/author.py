from tornado.web import RequestHandler
from datetime import datetime,timedelta
from afore.utils import G
from .answer import Rsp
import wrapt
import jwt
import os


class JWT():
    '''This json web token class.'''
    SECRET_KEY = os.urandom(24)
    def __init__(self) -> None:
        pass

    @wrapt.decorator
    @classmethod
    def jwt_sign_auth(cls,wrapped, instance:RequestHandler, args, kwargs):
        '''JWT签名认证-方法装饰器'''
        token = instance.request.headers.get('Authorization')
        if token:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=['HS256'])
            G.push_uid(value={payload['sub']:payload['uid']})
        else:
            Rsp.auth_fail()
        return wrapped(*args, **kwargs)



    @classmethod
    def jwt_login(cls,uid:int,sub,eff:int):
        ''' 登陆:
        uid 用户标示
        sub 面向用户，比如：super、client、customer
        eff 有效时间-秒
        '''
        this = cls()
        payload = {
            'uid': int(uid),
            'sub': sub,
            'exp': datetime.now() + timedelta(seconds=int(eff)),  # 过期时间 
            }
        token = jwt.encode(payload,this.SECRET_KEY,algorithm='HS256')
        return token

    @classmethod
    def jwt_refresh(cls,uid:int,eff:int):
        ''' 刷新:
        uid 用户标示
        eff 有效时间-秒
        '''
        this = cls()
        payload = {
            'uid': int(uid),
            'sub': 'refresh',
            'exp': datetime.now() + timedelta(seconds=int(eff)),  # 过期时间
            }
        token = jwt.encode(payload,this.SECRET_KEY,algorithm='HS256')
        return token

    @classmethod
    def jwt_decode(cls,token:str):
        ''' 解码:
        token 用户标示
        '''
        this = cls()
        payload = jwt.decode(token, this.SECRET_KEY, algorithms=['HS256'])
        return payload


