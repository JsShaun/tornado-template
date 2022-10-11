from tornado.web import Application

class AppT:
    '''路由器蓝图'''
    _RuleList =  []
    
    @classmethod
    def register_blueprint(cls,prefix="",rules=[]):
        newRules = [(prefix+url,view)  for url,view in rules]
        cls._RuleList.extend(newRules)
        return newRules

    @classmethod
    def make_app(cls):
        return Application(cls._RuleList)



