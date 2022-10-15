from afore.middleware import Rsp,JWT
from afore.utils import RqsH
from .server import DictS


class DictV(RqsH):
    @Rsp.response
    @JWT.jwt_sign_auth
    def post(self):
        """添加字典"""
        css = DictS()
        css.create(**self.jsBody)

    @Rsp.response
    @JWT.jwt_sign_auth
    def delete(self):
        """删除字典"""
        css = DictS()
        css.delete(**self.jsBody)
    
    @Rsp.response
    @JWT.jwt_sign_auth
    def put(self):
        """修改字典"""
        css = DictS()
        css.modify(**self.jsBody)

    @Rsp.response
    @JWT.jwt_sign_auth
    def get(self):
        """浏览字典"""
        css = DictS()
        css.browse(**self.jsQuery)

    @Rsp.response
    @JWT.jwt_sign_auth
    def options(self):
        """查找字典"""
        css = DictS()
        css.info(**self.jsQuery)


