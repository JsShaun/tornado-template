from utils.middleware import Rsp,R2H
from .server import RoomS


class RoomV(R2H):
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
    
