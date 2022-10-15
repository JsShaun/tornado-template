from bson import ObjectId
from model import GodotM
from afore.middleware import Rsp


class ActionS():
    """"""
    def __init__(self):
        self.obj = GodotM("Roles")

    def up_action(self,_id):
        '角色行为'
        where = {
            _id:ObjectId(_id)
        }
        action = {
            "Class": "Player",#类
            "Status":0,
            "Position": {"x":0,"y":0},#当前位置
            "Speed": {"x":0,"y":0},#当前速度
            "Back":{"x":0,"y":0},#后退
            "HP":10, #当前血量
            "MP":0,  #当前魔力值
            "ATN":1, #当前物理攻击力
            "INT":0, #当前魔法攻击力
        }

        unb = self.obj.update_one(where,{"$set":{'action':action}})
        Rsp.ok(unb)

