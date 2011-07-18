# -*- coding: utf-8 -*-
from _handler import LoginBase
from model.po_photo import po_photo_new
from model.cid import CID_PHOTO

def po_post(self):
    user_id = self.current_user_id
    name = self.get_argument('name', '')
    txt = self.get_argument('txt', '', strip=False).rstrip()
    arguments = self.request.arguments
    if secret:
        state = STATE_SECRET
    else:
        state = STATE_ACTIVE
    po = self.po_save(user_id, name, txt, state)
    self_id = self.id
    if po:
        po_id = po.id
        if not tag_id_by_po_id(user_id, po_id):
            zsite_tag_new_by_tag_id(po)
    else:
        po_id = 0
    if po or self_id == 0:
        update_pic(arguments, user_id, po_id, self_id)
        mc_pic_id_list.delete('%s_%s' % (user_id, self_id))
    return po

class PoPhoto(LoginBase):
    def post(self):


@urlmap('/po/photo')
class PoPhoto(LoginBase):
    def post(self, id=0):
        cid = CID_PHOTO
        template = 'ctrl/me/po/photo'
        po_save = staticmethod(po_photo_new)
        po = self.po_post()
        #USER DUMPS FIX HEADER FOR FIREFOX
        if id:
            id = int(id)
        r = self._post(id)
        if isinstance(r, (int, long)):
            r = {'status':r}
        r = dumps(r)
        self.finish(r)

    def _post(self, id):
        user_id = self.current_user_id

        files = self.request.files
        img = files.get('img')
        if img:
            img = img[0]['body']
        else:
            return 0

        if len(img) > 1024*1024*12:
            return 2

        img = picopen(img)
        if not img:
            return 10

        if id:
            po = Po.mc_get(id)
            if not po or po.user_id != user_id or (po.cid == CID_WORD and po.rid == 0):
                return 0
            if po.cid == CID_WORD:
                answer_word2note(po)

        if not pic_can_add(user_id, id):
            return 16

        pic = po_pic_new(user_id, id, img)
        if not pic:
            return 14

        r = {
            'status': 0,
            'src': fs_url_jpg(219, pic.id),
            'seqid': pic.seq,
        }

        return r
