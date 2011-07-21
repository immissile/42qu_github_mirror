# -*- coding: utf-8 -*-
from _handler import LoginBase
from ctrl._urlmap.me import urlmap
from model.fs import fs_url_jpg
from model.po_photo import photo_new
from model.po import Po, po_photo_new
from model.zsite_tag import zsite_tag_new_by_tag_id
from model.cid import CID_PHOTO
from model.state import STATE_ACTIVE
from zkit.pic import picopen

@urlmap('/po/photo')
@urlmap('/po/photo/(\d+)')
class PoPhoto(LoginBase):
    def post(self, po_id=0):
        cid = CID_PHOTO
        title = self.get_argument('name', None)
        txt = self.get_argument('txt', None)
        if po_id:
            po_id = int(po_id)
            po = Po.get(id=po_id) 
            if po.user_id == self.current_user_id:
                po.name_ = title
                po.txt_set(txt)
                po.save()
            else:
                return self.redirect('/live')
        else:
            img = self.check_img()
            if img:
                user_id = self.current_user_id
                photo_id = photo_new(user_id, img)
                po = po_photo_new(user_id, title, txt, photo_id, STATE_ACTIVE)
                zsite_tag_new_by_tag_id(po, 1)
                po_id = po.id
            else:
                return self.redirect('/live')
        return self.redirect('/po/tag/%s' % po_id)
        
    def check_img(self):
        files = self.request.files
        img = files.get('photo')
        if img:
            img = img[0]['body']
            if not len(img) > 1024*1024*12:
                img = picopen(img)
                if not img:
                    return
                return img
