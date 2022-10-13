from asyncinit import asyncinit
from config.local import UDP
import trio
from queue import Queue
from model.buffer import Buf,Msg
from . import transform
from . import process

class Channel:
    def __init__(self):
        self.send_channel, self.receive_channel = trio.open_memory_channel(0)
        
    async def upload(self,buf:Buf):
        await self.send_channel.send(buf)

    async def down(self):
        async for value in self.receive_channel:
            yield value


class DataStamp:
    """数据印记：
    用于需要重复发送次数标记
    数据形式：{"数据MD5":3}
    用于确认UDP回复通道
    - md5_set 回复确认设置，否则每两秒再发送一次，一共发送3次，期间有确认停止发送.使用buf.to_md5()获得并设置MD5
    """
    def __init__(self):
        self.q = Queue()
        self.md5_dict = dict()

    def qsize(self):
        """当前通道个数"""
        return self.q.qsize()

    def remove(self,md5):
        self.md5_dict.pop(md5,None)

    def upload(self,buf:Buf):
        """上传Key:Value，初始标记3"""
        if buf.md5 is None:
            self.md5_dict[buf.to_md5()] = 3
        self.q.put(buf)

    def down(self):
        """下载数据，标记减一。如果标记为零，则将Key:Value抹除"""
        buf:Buf = self.q.get()
        seq = self.md5_dict.get(buf.md5,0) - 1
        if seq >= 0:
            self.md5_dict[buf.md5] = seq
            self.upload(buf)
            return buf
        else:
            self.md5_dict.pop(buf.md5,None)

        

@asyncinit
class Task:
    send_channel = Channel()
    receive_channel = Channel()
    check_queue = DataStamp()

    async def __init__(self):
        """启动UDP服务"""
        print("启动UDP服务，地址为UDP：",UDP.HOST, UDP.PORT)
        sock = trio.socket.socket(trio.socket.AF_INET, trio.socket.SOCK_DGRAM)
        await sock.bind((UDP.HOST, UDP.PORT))
        async with trio.open_nursery() as nursery:
            nursery.start_soon(transform.receiver,sock,self.receive_channel)
            nursery.start_soon(transform.sender,sock,self.send_channel,self.check_queue)
            nursery.start_soon(transform.checker,sock,self.check_queue)
            nursery.start_soon(process.exec,self.send_channel,self.receive_channel,self.check_queue)