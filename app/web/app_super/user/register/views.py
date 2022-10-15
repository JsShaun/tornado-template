
from afore.middleware import Rsp,JWT
from afore.utils import RqsH
from .server import RegisterS


class RegisterV(RqsH):
    @Rsp.response
    @JWT.jwt_sign_auth
    def post(self):
        """用户注册"""

        css = RegisterS()
        css.create(**self.jsBody)

    @Rsp.response
    @JWT.jwt_sign_auth
    def delete(self):
        """用户删除"""
        css = RegisterS()
        css.delete(**self.jsBody)
    
    @Rsp.response
    @JWT.jwt_sign_auth
    def put(self):
        """用户修改"""
        css = RegisterS()
        css.modify(**self.jsBody)

    @Rsp.response
    @JWT.jwt_sign_auth
    def get(self):
        """注册用户查看"""

        css = RegisterS()
        css.browse(**self.jsQuery)

    @Rsp.response
    @JWT.jwt_sign_auth
    def options(self):
        """用户信息"""

        css = RegisterS()
        css.find(**self.jsQuery)


