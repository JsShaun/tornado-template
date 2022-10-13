from utils.middleware import Rsp,JWT,R2H
from tornado.web import RequestHandler
from .server import CityS


class CityV(R2H):
    """市"""
    @Rsp.response
    @JWT.jwt_sign_auth
    def get(self):
        """浏览城市"""
        css = CityS()
        css.browse(**self.jsQuery)


