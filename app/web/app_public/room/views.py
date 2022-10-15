from afore.middleware import Rsp,JWT
from afore.utils import RqsH
from .server import RoomS


class RoomV(RqsH):
    @Rsp.response
    def put(self):
        """进入房间"""
        css = RoomS()
        
        css.join(**self.jsBody)

    @Rsp.response
    def delete(self):
        """离开房间"""
        css = RoomS()
        css.leave(**self.jsBody)
    
