from utils.middleware import Rsp,R2H
from .server import ActionS

class ActionV(R2H):

    @Rsp.response
    def post(self):
        """更新角色行为"""
        css = ActionS()
        css.up_action(**self.jsBody)
    