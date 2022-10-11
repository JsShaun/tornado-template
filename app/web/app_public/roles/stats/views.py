from utils.middleware import Rsp,R2H
from .server import StatsS


class StatsV(R2H):

    @Rsp.response
    def post(self):
        """更新角色属性"""
        css = StatsS()
        css.up_stats(**self.jsBody)
    