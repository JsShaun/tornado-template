from model import PublicM
from utils.middleware import Rsp


class CountyS():
    def __init__(self):
        self.obj = PublicM(table="county")

    def browse(self,city_code=None,size=100,offset=1):
        sql = """
        SELECT county_code,county_name
        FROM "public".county
        WHERE is_delete IS FALSE
        {0} AND "city_code" = %(city_code)s
        """.format(
            '--' if city_code is None else ''
        )
        data = self.obj.select(sql,params={"size":size,"offset":offset,"city_code":city_code})
        Rsp.ok(data)

 
        



