from afore.middleware import Rsp,JWT
from afore.utils import RqsH
from .server import ActionS

class ActionV(RqsH):

    @Rsp.response
    def post(self):
        """更新角色行为"""
        css = ActionS()
        css.up_action(**self.jsBody)
    