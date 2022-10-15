from afore.middleware import Rsp,JWT
from afore.utils import RqsH
from .server import CityS


class CityV(RqsH):
    """市"""
    @Rsp.response
    @JWT.jwt_sign_auth
    def get(self):
        """浏览城市"""
        css = CityS()
        css.browse(**self.jsQuery)



