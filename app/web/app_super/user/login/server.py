
import pandas as pd
from utils.middleware import JWT,Rsp
from model import SuperM


class LoginS():
    """用户登陆"""
    def __init__(self):
        self.obj = SuperM(table='user')
 
    def sign_in(self,email,pass_word):
        
        '''用户登陆；获取token；权限缓存'''
        data = dict()
        sql = """
        select "id","phone","pass_word",100000 as expired
        from "super"."user" 
        where is_delete IS FALSE AND "email" = %(email)s
        """
        
        for _,ss in self.obj.data_frame(sql,params={"email":email}).iterrows():
            if pass_word != ss['pass_word']:
                Rsp.login_fail()
            # self.data_power(uid=ss['id'],expired=ss['expired'])
            data['login_token'] = JWT.jwt_login(uid=ss['id'],sub="super",eff=1000)
            data['login_expired'] = 100000
            data['refresh_token'] = JWT.jwt_refresh(uid=ss['id'],eff=ss['expired'])
            Rsp.ok(data)
        else:
            Rsp.login_fail()


    def data_power(self,uid,expired=None):
        '''数据权限缓存'''
        sql = '''
        WITH RECURSIVE F AS (
            SELECT "id"
            FROM super."user"
            WHERE is_delete IS FALSE AND "creator" = %(uid)s
            UNION
            SELECT U."id"
            FROM super."user" U
            JOIN F ON F."id" = U.creator
            WHERE U.is_delete IS FALSE
        )
        SELECT "id" AS uid FROM F
        '''
        df = self.obj.con.pandas(sql,params={"uid":uid})
        alias = "dp:{}".format(uid)
        ex = pd.Timedelta(value=expired,unit="S")
        return self.obj.session.store_series(alias=alias,local_series=df['uid'],ex=ex)

    
    def sign_out(self):
        '''用户登出；清除缓存'''
        alias = "dp:{}".format(self.obj.uid)
        Rsp.ok(data=self.obj.session.delete(alias),msg="注销成功")
    
    def sign_new(self,refresh_token):
        '''刷新验证；获取新的Token'''
        data = dict()
        payload = JWT.jwt_decode(refresh_token)
        if payload['sub'] != "refresh":
            raise Rsp.invalid_token()
        data['login_token'] = JWT.jwt_login(uid=payload["uid"],sub="super",eff=1000)
        data['login_expired'] = 1000
        Rsp.ok(data)

    
    def sign_info(self):
        '登陆信息获取'
        data = dict()
        sql = '''
        SELECT "id",email,last_time,create_time
        FROM super."user"
        WHERE is_delete IS FALSE AND id = %(uid)s
        '''
        data['登录'] = self.obj.first(sql,params={"uid":self.obj.uid}).to_dict()

        alias = "dp:{}".format(self.obj.uid)
        # if not self.obj.session.exists(alias):
        #     Rsp.no_power(msg='当前账号已注销')
        # s2 = self.obj.session.load_series(alias)
        # data['权限'] = s2.to_list()
        Rsp.ok(data)

    def sign_password(self,pass_word):
        '修改登录密码'
        Rsp.ok(data=self.obj.update(id=self.obj.uid,pass_word=pass_word),msg="密码修改成功")
