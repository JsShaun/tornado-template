from afore.middleware import Rsp,JWT
from afore.utils import RqsH
from .server import LoginS

class LoginV(RqsH):
    
    @Rsp.response
    def post(self):
        '用户登陆'
        css = LoginS()
        css.sign_in(**self.jsBody)

    @Rsp.response
    @JWT.jwt_sign_auth
    def delete(self):
        '登陆注销'
        css = LoginS()
        css.sign_out()
    
    @Rsp.response
    def options(self):
        '刷新验证'
        css = LoginS()
        css.sign_new(**self.jsBody)

    @Rsp.response
    @JWT.jwt_sign_auth
    def get(self):
        '登录信息'
        css = LoginS()
        css.sign_info()
        
       
    @Rsp.response
    @JWT.jwt_sign_auth
    def put(self):
        '修改登录密码'
        css = LoginS()
        css.sign_password(**self.jsBody)
        


