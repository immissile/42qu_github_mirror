# -*- coding: utf-8 -*-
from _handler import LoginBase
from ctrl._urlmap.me import urlmap
from model.fs import fs_url_jpg
from model.po_photo import photo_new
from model.po import Po, po_photo_new
from model.cid import CID_PHOTO
from model.state import STATE_ACTIVE
from zkit.pic import picopen

@urlmap('/po/photo')
@urlmap('/po/photo/(\d+)')
class PoPhoto(LoginBase):
    def post(self, po_id=0):
        cid = CID_PHOTO
        user_id = self.zsite_id
        title = self.get_argument('name', None)
        txt = self.get_argument('txt', None)
        img = self.check_img()
        if title and txt and img:
            photo_id = photo_new(user_id, img)
            if po_id:
                #edit
                po_id = int(po_id)
                po = Po.get(id=po_id) 
                po.user_id = user_id
                po.name = title
                po.txt = txt
                po.rid = photo_id 
                po.save()
            else:
                #new
                po = po_photo_new(user_id, title, txt, photo_id, STATE_ACTIVE)
                po_id = po.id
            self.redirect('/po/tag/%s' % po_id)
        
    def check_img(self):
        files = self.request.files
        img = files.get('photo')
        if img:
            img = img[0]['body']
        else:
            return None

        if len(img) > 1024*1024*12:
            return None

        img = picopen(img)
        if not img:
            return None
        
        return img
