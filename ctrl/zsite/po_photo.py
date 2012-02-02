# -*- coding: utf-8 -*-
from _handler import ZsiteBase, LoginBase, XsrfGetBase, login
from ctrl._urlmap.zsite import urlmap
from model.zsite_site import zsite_id_by_zsite_user_id
from model.fs import fs_url_jpg
from model.po_photo import po_photo_new
from model.po import Po
from model.cid import CID_PHOTO
from model.state import STATE_ACTIVE, STATE_PO_ZSITE_SHOW_THEN_REVIEW
from zkit.pic import picopen

@urlmap('/po/photo')
@urlmap('/po/photo/(\d+)')
class PoPhoto(LoginBase):
    def post(self, po_id=0):
        cid = CID_PHOTO
        name = self.get_argument('name', None)
        txt = self.get_argument('txt', None)
        user_id = self.current_user_id


        link = '/feed'

        if po_id:
            po_id = int(po_id)
            po = Po.mc_get(po_id)
            if po and po.user_id == user_id:
                po.name_ = name
                po.txt_set(txt)
                po.save()
                link = '/po/tag/%s' % po_id
        else:
            img = self._img()
            if img:
                zsite_id = zsite_id_by_zsite_user_id(self.zsite, user_id)
                if zsite_id:
                    state = STATE_PO_ZSITE_SHOW_THEN_REVIEW
                else:
                    state = STATE_ACTIVE
                po = po_photo_new(user_id, name, txt, img, state, zsite_id)
                if po:
                    po_id = po.id

                    link = '/po/tag/%s' % po_id


        return self.redirect(link)

    def _img(self):
        files = self.request.files
        img = files.get('photo')
        if img:
            img = img[0]['body']
            if not len(img) > 1024*1024*12:
                img = picopen(img)
                if not img:
                    return
                return img



