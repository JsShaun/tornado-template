from afore.middleware import Rsp,JWT
from afore.utils import RqsH
from .server import ProvinceS


class ProvinceV(R2H):
    """省"""
    @Rsp.response
    @JWT.jwt_sign_auth
    def get(self):
        """浏览省份"""
        css = ProvinceS()
        css.browse(**self.jsQuery)




