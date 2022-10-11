from model import GodotM
import pandas as pd
from model.buffer import Msg

class Room:

    def __init__(self):
        self.obj = GodotM("Room")

    def ask(self,ip,port,room_key):
        """房间请求"""

        # 查询mongo房间数据
        rst = self.obj.first({"key":room_key})
        if rst.empty:
            rst['key'] = room_key
            rst['ip_list'] = []

        # IP列表转DF处理数据
        df1 = pd.DataFrame(rst['ip_list'],columns=['ip','port','time'])
        df2 = df1.drop(df1.query("ip == '{}' & port == {:.0f}".format(ip,port)).index)
        
        df3 = df2[df2['time'].apply(lambda x: x + 60 > self.obj.timestamp)]
        df3_1 = pd.json_normalize([{"ip":ip,"port":port,"time":self.obj.timestamp}])

        df4 = pd.concat([df3,df3_1])
        # 强制转换类型
        df4['port'] = df4['port'].apply(lambda x:int(x))
        df4['time'] = df4['time'].apply(lambda x:int(x))

        
        # 转换为Json类型，保存mongo
        rst['ip_list'] = df4.to_dict('records')
        self.obj.save(rst.to_dict())

        # 所有的IP需要得到通知
        df5 = df4[['ip','port']]
        df5.reset_index(drop=True, inplace=True)
        for i,ss in df5.iterrows():
            df5_1 = df5.drop([i])
            smsg = Msg.new(ip=ss['ip'],port=ss['port'],type="ROOM-RSP")
            obj = {"myself":ss.to_dict(),"ip_list":df5_1.to_dict('records')}
            yield smsg.set_object(obj=obj)



        
