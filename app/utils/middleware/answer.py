from tornado.web import RequestHandler
from tornado.escape import json_decode
from .buffer import G
import wrapt
from json import dumps,JSONEncoder
import pandas as pd
import numpy as np
from datetime import date,datetime
import decimal
from bson import ObjectId
from jwt.exceptions import (
    InvalidTokenError, DecodeError, InvalidAlgorithmError,
    InvalidAudienceError, ExpiredSignatureError, ImmatureSignatureError,
    InvalidIssuedAtError, InvalidIssuerError, MissingRequiredClaimError,
    InvalidSignatureError, PyJWTError
)



class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if pd.isnull(obj):
            return 'null'
        if isinstance(obj, date):  
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        elif isinstance(obj, np.generic):
            return obj.item()
        elif isinstance(obj, ObjectId):
            return str(obj)
        else:
            return JSONEncoder.default(self, obj)



class Rsp(Exception):
    """Response
    # http://tools.jb51.net/table/http_status_code
    1**	信息,服务器收到请求,需要请求者继续执行操作
    2**	成功,操作被成功接收并处理
    3**	重定向,需要进一步的操作以完成请求
    4**	客户端错误,请求包含语法错误或无法完成请求
    5**	服务器错误,服务器在处理请求的过程中发生了错误
    """
    def __init__(self,code=0,message='',data=None):
        super().__init__(code,message,data)
        self.code = code
        self.message = message
        self.data = data
 

    @classmethod
    def next(cls,msg='',data=None):
        '继续。客户端应继续其请求。'
        result = {"code": 100, "message": "继续。", "data": data}
        if msg:
            result["message"] = msg
        this = cls(**result)
        raise this

    @classmethod
    def exchange(cls,msg='',data=None):
        '切换协议。服务器根据客户端的请求切换协议。只能切换到更高级的协议,例如,切换到HTTP的新版本协议。'
        result = {"code": 101, "message": "切换协议。", "data": data}
        if msg:
            result["message"] = msg
        this = cls(**result)
        raise this


    @classmethod
    def ok(cls,data=None,msg=""):
        '请求成功,正常返回。'
        result = {"code": 200,"message": msg,"data":data}
        this = cls(**result)
        raise this

    @classmethod
    def customize(cls,code,message,data):
        '自定义返回'
        this = cls(code,message,data)
        raise this  
    
    @classmethod
    def login_fail(cls,msg='',data=None):
        '登录失败'
        result = {"code": 203, "message": "密码或账号错误", "data": data}
        if msg:
            result["message"] = msg
        this = cls(**result)
        raise this

    @classmethod
    def no_content(cls,msg='',data=None):
        '无内容。服务器成功处理,但未返回内容。在未更新网页的情况下,可确保浏览器继续显示当前文档'
        result = {"code": 204, "message": "无内容。服务器成功处理,但未返回内容。", "data": data}
        if msg:
            result["message"] = msg
        this = cls(**result)
        raise this
        
    @classmethod
    def auth_fail(cls,msg='',data=None):
        '认证失败'
        result = {"code": 332,  "message": "请输入 Headers Authorization: {token}", "data": data}
        if msg:
            result["message"] = msg
        this = cls(**result)
        raise this

    @classmethod
    def sign_fail(cls,msg='',data=None):
        '验签失效'
        result = {"code": 333, "message": "验签失效, 请重新登录!", "data": data}
        if msg:
            result["message"] = msg
        this = cls(**result)
        raise this
    
    @classmethod
    def invalid_token(cls,msg='',data=None):
        '无效Token'
        result = {"code": 334, "message": "无效Token,请验证Token!", "data": data}
        if msg:
            result["message"] = msg
        this = cls(**result)
        raise this

    @classmethod
    def no_power(cls,msg='',data=None):
        '没有权限'
        result = {"code": 335, "message": "没有权限!", "data": data}
        if msg:
            result["message"] = msg
        this = cls(**result)
        raise this

    @classmethod
    def repeat(cls,msg='',data=None):
        '数据重复'
        result = {"code": 336, "message": "数据已存在!", "data": data}
        if msg:
            result["message"] = msg
        this = cls(**result)
        raise this
    
    @classmethod
    def keynull(cls,msg='',data=None):
        '缺少字段'
        result = {"code": 337, "message": "缺少字段和值!", "data": data}
        if msg:
            result["message"] = msg
        this = cls(**result)
        raise this

    @classmethod
    def operate(cls,msg='',data=None):
        '操作不成功'
        result = {"code": 338, "message": "操作失败!", "data": data}
        if msg:
            result["message"] = msg
        this = cls(**result)
        raise this

    @classmethod
    def weixin(cls,msg="",data=None):
        '微信错误'
        result = {"code": 350, "message": "微信认证错误!", "data": data}
        if msg:
            result["message"] = msg
        this = cls(**result)
        raise this

    @wrapt.decorator
    @classmethod
    async def response(cls,wrapped, instance:RequestHandler, args, kwargs):
        '''返回对应响应信息,拦截异常'''
        try:
            await wrapped(*args, **kwargs)
            
        except cls as p:
            result = {"code": p.code, "message": p.message, "data": p.data}
            instance.write(dumps(result, cls=CustomJSONEncoder))

        except ExpiredSignatureError as e:
            result = {"code": 333, "message": "登录验证已失效,请重新登录", "data": None}
            instance.write(dumps(result, cls=CustomJSONEncoder))
        
        except InvalidTokenError as e:
            result = {"code": 334, "message": "Token验证不通过!", "data": str(e)}
            instance.write(dumps(result, cls=CustomJSONEncoder))
        
        except TypeError as e:
            result = {"code": 406, "message": "wrapped: " + str(wrapped) + ". message: " + str(e), "data": None}
            instance.write(dumps(result, cls=CustomJSONEncoder))

        except Exception as e:
            result = {"code": 500, "message": "wrapped: " + str(wrapped) + ". message: " + str(e), "data": None}
            instance.write(dumps(result, cls=CustomJSONEncoder))

        else:
            result = {"code": 501, "message": "未返回任何信息", "data": None}
            instance.write(dumps(result, cls=CustomJSONEncoder))
        
        finally:
            G.freed_uid()


class Rhandler(RequestHandler):
    def prepare(self):
        content_type:str = self.request.headers.get("content-type","")
        if content_type.startswith('application/json'):
            body = self.request.body
            self.jsBody = json_decode(body) if body else {}
        self.jsQuery = { k: self.get_argument(k) for k in self.request.arguments }
        
        

        
