from model import PublicM
from utils.middleware import Rsp


class CityS():
    def __init__(self):
        self.obj = PublicM(table="city")

    def browse(self,province_code=None,size=100,offset=1):
        sql = """
        SELECT city_code,city_name
        FROM "public".city
        WHERE is_delete IS FALSE
        {0} AND "province_code" = %(province_code)s
        """.format(
            '--' if province_code is None else ''
        )
        data = self.obj.select(sql,params={"size":size,"offset":offset,"province_code":province_code})
        Rsp.ok(data)


 
        



