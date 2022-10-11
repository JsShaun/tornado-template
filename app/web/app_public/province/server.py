from model import PublicM
from utils.middleware import Rsp


class ProvinceS():
    def __init__(self):
        self.obj = PublicM(table="province")
        

    def browse(self,size=100,offset=1):
        sql = """
        SELECT province_code,province_name
        FROM "public".province
        WHERE is_delete IS FALSE AND is_open IS TRUE
        """
        data = self.obj.select(sql,params={"size":size,"offset":offset})
        Rsp.ok(data)


 