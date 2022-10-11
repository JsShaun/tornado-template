from bson import ObjectId
from model import GodotM
from utils.middleware import Rsp

class StatsS():
    """"""
    def __init__(self):
        self.obj = GodotM("Roles")

    def up_stats(self,_id):
        where = {
            _id:ObjectId(_id)
        }
        stats = {
            "MAX_HP":10,#生命值上限
            "MAX_MP":0,#魔力上限
            "PHY":1,#体魄
            "SPI":1,#精神
            "AGILE":1,#灵巧
            "SPEED":70,#移动速度
            "SIGHT":80,#感知
            "LUCKY":0,#幸运值
            "WEIGHT":50,#体重Kg
        }

        unb = self.obj.update_one(where,{"$set":{'stats':stats}})
        Rsp.ok(unb)



        
        



