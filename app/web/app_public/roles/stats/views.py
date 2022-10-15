from afore.middleware import Rsp,JWT
from afore.utils import RqsH
from .server import StatsS


class StatsV(RqsH):

    @Rsp.response
    def post(self):
        """更新角色属性"""
        css = StatsS()
        css.up_stats(**self.jsBody)
    