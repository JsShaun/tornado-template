from dataclasses import dataclass
import json
import hashlib

@dataclass
class Buf:
    """UDP
    接收数据载体
    ip:port 发送地址
    data 发送数据（字节码）
    """
    ip:str
    port:int
    data:bytes
    md5:str=None

    def to_msg(self):
        '''解码data数据,返回Msg对象'''
        data:dict = json.loads(self.data.strip(b'0'))
        return Msg(self.ip,self.port,data)

    def to_md5(self)->str:
        """获得并设置MD5"""
        self.md5 = hashlib.md5(self.data).hexdigest()
        return self.md5


@dataclass
class Msg:
    '''UDP
    发送数据载体
    ip:port 接收源地址
    type 数据类型，用于后续解码
    '''
    ip:str
    port:int
    data:dict

    @classmethod
    def new(cls,ip:str,port:int,type:str):
        self = cls(ip,port,data={'type':type})
        return self
    
    def set_object(self,obj):
        '''上传object对象'''
        obj = json.dumps(obj)
        self.data['object'] = obj
        return self

    def get_type(self)->str:
        """获取协议对象"""
        if 'type' in self.data.keys():
            return self.data['type']

    def to_buf(self):
        '''将data数据转为字节码，用以UDP传输'''
        data = bytes(json.dumps(self.data),'utf8')
        return Buf(self.ip,self.port,data)

    def get_object(self):
        '''解码object对象'''
        if 'object' in self.data.keys():
            obj = json.loads(self.data['object'])
            self.data['object'] = obj
            return obj