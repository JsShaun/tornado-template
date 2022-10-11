from model.buffer import Msg
from .room import Room
import re




async def exec(send_channel,receive_channel,check_queue):
    async for buf in receive_channel.down():
        msg:Msg = buf.to_msg()
        print("UDP接收请求数据:",msg)

        if 'type' not in msg.data.keys():
            smsg = Msg.new(msg.ip,msg.port,type="Null")
            await send_channel.upload(smsg.to_buf())
            continue

        type1 = msg.data['type']
        
        # IP请求协议
        if type1 == "IP-ASK":
            smsg = Msg.new(msg.ip,msg.port,type="IP-RSP")
            smsg.set_object(obj={"ip":msg.ip,"port":msg.port})
            buf = smsg.to_buf()
            await send_channel.upload(buf)

        # 接收房间请求
        elif type1 == "ROOM-ASK":
            room_key = msg.data.get('ROOM')
            if room_key:
                room = Room()
                # 分别发送msg
                for smsg in room.ask(msg.ip,msg.port,room_key):
                    buf = smsg.to_buf()
                    await send_channel.upload(buf)
                    check_queue.upload(buf)

        # 房间请求确认
        elif type1 == "ROOM-CHK":
            md5 = msg.data.get('MD5')
            if md5:
                # print("回复确认. 清除md5:",md5)
                check_queue.remove(md5)

        # 数据中转
        elif type1 == "ACTION-NEW":
            target = msg.data.pop("target",None) # 目标地址
            if target:
                ip, port = re.split(':', target)
                msg.ip = ip
                msg.port = port
                buf = msg.to_buf()
                # print("中转数据：",buf)
                await send_channel.upload(buf)


        # 请求协议不存在
        else:
            smsg = Msg.new(msg.ip,msg.port,type="Unk")
            send_channel.upload(smsg.to_buf())


                
            


            