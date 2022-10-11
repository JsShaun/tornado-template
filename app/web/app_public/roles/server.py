from bson import ObjectId
from model import GodotM
from utils.middleware import Rsp
import pandas as pd


class RolesS():
    """"""
    def __init__(self):
        self.obj = GodotM("Roles")

    def roles_view(self,user_id):
        '查看角色'
        rst = self.obj.select({"user_id":ObjectId(user_id)})
        Rsp.ok(rst.to_dict('records'))

    def new_role(self,name:str,user_id):
        '创建角色'

        role = {"room_key":0,"user_id":ObjectId(user_id)}
        role['action'] = {
            "Class": "Player",#类
            "Name": name,#玩家名称
            "Status":0,
            "Position": {"x":0,"y":0},#当前位置
            "Speed": {"x":0,"y":0},#当前速度
            "Back":{"x":0,"y":0},#后退
            "HP":10, #当前血量
            "MP":0,  #当前魔力值
            "ATN":1, #当前物理攻击力
            "INT":0, #当前魔法攻击力
        }
        role['stats'] = {
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

        oid = self.obj.insert_one(role)
        Rsp.ok(oid)



        
        



