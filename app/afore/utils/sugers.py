from tornado.web import Application
from tornado.web import RequestHandler
from tornado.escape import json_decode


class AppT:
    '''路由器蓝图'''
    _rule_list =  []
    
    @classmethod
    def register_blueprint(cls,prefix="",rules=[]):
        new_rules = [ ( prefix + url,view )  for url, view in rules]
        cls._rule_list.extend(new_rules)
        return new_rules

    @classmethod
    def make_app(cls):
        return Application(cls._rule_list)


class RqsH(RequestHandler):
    '''请求处理基类'''
    def prepare(self):
        content_type:str = self.request.headers.get("content-type","")
        if content_type.startswith('application/json'):
            body = self.request.body
            self.jsBody = json_decode(body) if body else {}
        self.jsQuery = { k: self.get_argument(k) for k in self.request.arguments }