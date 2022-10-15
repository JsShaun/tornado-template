from afore.middleware import Rsp,JWT
from afore.utils import RqsH
from .server import RolesS


class RolesV(RqsH):
    @Rsp.response
    def get(self):
        """浏览角色"""
        css = RolesS()
        css.roles_view(**self.jsQuery)

    @Rsp.response
    def post(self):
        """创建角色"""
        css = RolesS()
        css.new_role(**self.jsBody)
    