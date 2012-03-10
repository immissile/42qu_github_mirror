#coding:utf-8
from _handler import JLoginBase, Base
from ctrl._util.star import can_admin_json
from ctrl._urlmap.j import urlmap

@urlmap('/j/star/(\d+)/pp/upload')
@urlmap('/j/star/(\d+)/po/upload/(\d+)')
class Upload(JLoginBase):
    @can_admin_json
    def post(self, id, po_id=0):
        pass 

@urlmap('/j/star/(\d+)/po/upload/rm')
@urlmap('/j/star/(\d+)/po/upload/rm/(\d+)')
class UploadRm(JLoginBase):
    @can_admin_json
    def post(self, id, po_id=0):
        pass 

