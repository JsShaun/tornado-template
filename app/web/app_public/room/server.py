from model import GodotM
from afore.middleware import Rsp
import pandas as pd
from model.buffer import Msg,Send

class RoomS():
    """"""
    def __init__(self):
        self.obj = GodotM("Room")

    def join(self,key,ip,port):
        '进入房间'

        rst = self.obj.first({"key":key})
        if rst.empty:
            rst['key'] = key
            rst['ip_list'] = []

        df1 = pd.DataFrame(rst['ip_list'],columns=['ip','port','time'])
        df2 = df1.drop(df1.query("ip == '{}' & port == {:.0f}".format(ip,port)).index)

        df3 = df2[df2['time'].apply(lambda x: x + 60 > self.obj.timestamp)]
        df4 = df3.append({"ip":ip,"port":port,"time":self.obj.timestamp},ignore_index=True)

        df4['port'] = df4['port'].apply(lambda x:int(x))
        df4['time'] = df4['time'].apply(lambda x:int(x))

        for _,ss in df4.iterrows():
            smsg = Msg.new(ip=ss['ip'],port=ss['port'],type="ROOM-NEW")
            smsg.set_object(obj=df4[['ip','port']].to_dict('records'))
            Send.upload(smsg.to_buf())

        rst['ip_list'] = df4.to_dict('records')
        self.obj.save(rst.to_dict())
        Rsp.ok(rst.to_dict())

    def leave(self,key,ip,port):
        '离开房间'
        rst = self.obj.first({"key":key})
        if rst.empty:
            rst['key'] = key
            rst['ip_list'] = []

        df1 = pd.DataFrame(rst['ip_list'],columns=['ip','port','time'])
        df2 = df1.drop(df1.query("ip == '{}' & port == {:.0f}".format(ip,port)).index)
        df4 = df2[df2['time'].apply(lambda x: x + 60 > self.obj.timestamp)]

        df4['port'] = df4['port'].apply(lambda x:int(x))
        df4['time'] = df4['time'].apply(lambda x:int(x))

        for _,ss in df4.iterrows():
            smsg = Msg.new(ip=ss['ip'],port=ss['port'],type="ROOM-NEW")
            smsg.set_object(obj=df4[['ip','port']].to_dict('records'))
            Send.upload(smsg.to_buf())

        rst['ip_list'] = df4.to_dict('records')
        self.obj.save(rst.to_dict())
        Rsp.ok(rst.to_dict())

        
        



