from utils.middleware import Rsp,R2H
from .server import LoginS



class VisitV(R2H):

    @Rsp.response
    async def post(self):
        '临时用户登陆'
        css = LoginS()
        await css.visit_in(**self.jsBody)
