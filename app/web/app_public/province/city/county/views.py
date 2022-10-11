from utils.middleware import Rsp,JWT,R2H
from tornado.web import RequestHandler
from .server import CountyS


class CountyV(R2H):
    "区"
    @Rsp.response
    @JWT.jwt_sign_auth
    def get(self):
        """浏览县级"""
        css = CountyS()
        css.browse(**self.jsQuery)




