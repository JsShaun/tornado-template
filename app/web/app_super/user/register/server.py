from model import SuperM
from utils.middleware import Rsp



class RegisterS():
    """子用户管理"""
    def __init__(self):
        self.obj = SuperM(table="user")

    def create(self,phone,email,pass_word):
        if self.obj.exist(params={"phone":phone}):
            Rsp.repeat("电话已注册")
        if self.obj.exist(params={"email":email}):
            Rsp.repeat("邮箱已注册")
        nid = self.obj.insert(phone=phone,email=email,pass_word=pass_word)
        Rsp.ok(nid,msg='注册成功。')

    def delete(self,id):
        if isinstance(id,(tuple,list)):
            rowcount = self.obj.delete(*id)
        else:
            rowcount = self.obj.delete(id)
        Rsp.ok(rowcount)

    def modify(self,id,phone=None,email=None,pass_word=None,city_manager=None):
        if phone:
            if self.obj.exist(params={"phone":phone}):
                Rsp.repeat("电话已注册")
        if email:
            if self.obj.exist(params={"email":email}):
                Rsp.repeat("邮箱已注册")
        rowcount = self.obj.update(id=id,phone=phone,email=email,pass_word=pass_word,city_manager=city_manager)
        Rsp.ok(rowcount)

    def find(self,id):
        rst = self.obj.echo(id).to_dict()
        Rsp.ok(rst)


    def browse(self,**kwargs):
        "查看子用户"
        sql = """
        SELECT usr.id,usr.phone,usr.email,usr.last_time,usr.create_time
        FROM super.user usr
        WHERE usr.is_delete IS False AND usr.creator = %(uid)s
        """
        data = self.obj.select(sql,params=kwargs)
        Rsp.ok(data)
            
        
        



