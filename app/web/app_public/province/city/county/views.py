from afore.middleware import Rsp,JWT
from afore.utils import RqsH
from tornado.web import RequestHandler
from .server import CountyS


class CountyV(RqsH):
    "区"
    @Rsp.response
    @JWT.jwt_sign_auth
    def get(self):
        """浏览县级"""
        css = CountyS()
        css.browse(**self.jsQuery)




