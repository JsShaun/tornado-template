from queue import Queue
from afore.cache import Buf,Msg


class Receive:
    """用于接收UDP通道"""
    __q = Queue()

    @classmethod
    def upload(cls,buf:Buf):
        cls.__q.put(buf)

    @classmethod
    def not_empty(cls):
        return not cls.__q.empty()

    @classmethod
    def down(cls)->Buf:
        return cls.__q.get()


class Send:
    """用于发送UDP通道"""
    __q = Queue()

    @classmethod
    def upload(cls,buf:Buf):
        cls.__q.put(buf)

    @classmethod
    def not_empty(cls):
        return not cls.__q.empty()

    @classmethod
    def down(cls)->Buf:
        return cls.__q.get()


class Check:
    """
    用于确认UDP回复通道
    - md5_set 回复确认设置，否则每两秒再发送一次，一共发送9次，期间有确认停止发送.使用buf.to_md5()获得并设置MD5
    """
    __q = Queue()
    md5_set = set()

    @classmethod
    def qsize(cls):
        """当前通道个数"""
        return cls.__q.qsize()

    @classmethod
    def upload(cls,seq:int,buf:Buf):
        """上传"""
        data = (seq,buf)
        cls.__q.put(data)

    @classmethod
    def not_empty(cls):
        """不为空"""
        return not cls.__q.empty()

    @classmethod
    def down(cls):
        """下载"""
        seq,buf = cls.__q.get()
        return (seq,buf)
