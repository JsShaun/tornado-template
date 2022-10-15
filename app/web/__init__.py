from tornado.httpserver import HTTPServer
import tornado.ioloop
import tornado.web
from afore.utils import AppT,RqsH
from . import app_public,app_super
from afore.config import Web


class Hello(RqsH):
    def get(self):
        self.write("Hello Tornado!!!")

AppT.register_blueprint(prefix=r"",rules=[(r"/", Hello),])
AppT.register_blueprint(prefix=r"/public",rules=app_public.RuleList)
AppT.register_blueprint(prefix=r"/super",rules=app_super.RuleList)


def start():
    print("启动web服务,地址为TCP:{}:{}".format(Web.HOST,Web.PORT))
    app = AppT.make_app()
    server = HTTPServer(app,xheaders=True)
    server.bind(Web.PORT,Web.HOST)
    server.start(1) # 线程数
    tornado.ioloop.IOLoop.current().start()
    
