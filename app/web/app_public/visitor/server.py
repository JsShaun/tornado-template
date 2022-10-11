from utils.middleware import JWT,Rsp
import asyncio


class LoginS():
    
    def __init__(self):
        pass

    async def visit_in(self):
        '''临时登录'''
        data = {}
        data['login_token'] = JWT.jwt_login(uid=0,sub="visit",eff=1000)
        data['login_expired'] = 100000
        data['refresh_token'] = JWT.jwt_refresh(uid=0,eff=100000)
        Rsp.ok(data)