from afore.middleware import Rsp,JWT
from afore.utils import RqsH
from .server import LoginS



class VisitV(RqsH):

    @Rsp.response
    async def post(self):
        '临时用户登陆'
        css = LoginS()
        await css.visit_in(**self.jsBody)
