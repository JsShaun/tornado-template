from model import PublicM
from utils.middleware import Rsp


class DictS():
    """数据字典关联，可以做Redis缓存"""
    def __init__(self):
        self.obj = PublicM(table="dictionary")

    def create(self,organize,options_value,options_label,father_value=None):
        if self.obj.exist(params={"organize":organize,"options_value":options_value}):
            Rsp.repeat("已存在字典！")
        iid = self.obj.insert(organize=organize,options_value=options_value,options_label=options_label,father_value=father_value)
        Rsp.ok(iid)

    def delete(self,id):
        if isinstance(id,(tuple,list)):
            rowcount = self.obj.delete(*id)
        else:
            rowcount = self.obj.delete(id)
        Rsp.ok(rowcount)


    def modify(self,id,options_label=None,organize_tab=None,father_value=None):
        if options_label:
            if self.obj.exist(params={"options_label":options_label}):
                Rsp.repeat("已经存在标签!")
        rowcount = self.obj.update(id=id,options_label=options_label,organize_tab=organize_tab,father_value=father_value)
        Rsp.ok(rowcount)


    def browse(self,organize=None,size=10,offset=1):
        sql = """
        SELECT *
        FROM "public"."dictionary"
        WHERE is_delete IS FALSE
        {0} AND "organize" = %(organize)s
        """.format(
            '--' if organize is None else ''
        )
        data = self.obj.select(sql,params={"organize":organize,"size":size,"offset":offset})
        Rsp.ok(data)


    def info(self,organize,father_value=None):
        sql = """
        SELECT options_value,options_label
        FROM "public"."dictionary"
        WHERE "organize" = %(organize)s
        {0} AND father_value = %(father_value)s
        """.format(
            '--' if father_value is None else ''
        )
        df1 = self.obj.con.pandas(sql,params={"organize":organize,"father_value":father_value})
        if df1.empty:
            Rsp.ok(data={})
        else:
            Rsp.ok(df1.to_dict('records'))
            
        
        



