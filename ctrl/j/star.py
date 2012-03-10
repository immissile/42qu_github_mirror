#coding:utf-8
from _handler import JLoginBase, Base
from ctrl._util.star import can_admin_json
from ctrl._util.po import pic_upload_rm
from ctrl._urlmap.j import urlmap
from ctrl._util.po import pic_upload_rm, pic_upload

@urlmap('/j/star/(\d+)/po/upload')
@urlmap('/j/star/(\d+)/po/upload/(\d+)')
class Upload(JLoginBase):
    @can_admin_json
    def post(self, id, po_id=0):
        zsite = self.zsite
        pic_upload(self, zsite.id, po_id)

@urlmap('/j/star/(\d+)/po/upload/rm')
@urlmap('/j/star/(\d+)/po/upload/rm/(\d+)')
class UploadRm(JLoginBase):
    @can_admin_json
    def post(self, id, po_id=0):
        zsite = self.zsite
        pic_upload_rm(self, zsite.id, po_id)

