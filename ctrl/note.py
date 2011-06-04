#!/usr/bin/env python
#coding:utf-8

import _handler
from zweb._urlmap import urlmap
from model.po import Po, po_rm,\
        po_note_new, STATE_SECRET, STATE_ACTIVE, po_state_set, CID_NOTE
from model.po_pic import  pic_list, pic_list_edit
from model import reply
from model.zsite import Zsite
from zkit.jsdict import JsDict



@urlmap("/po/note")
@urlmap("/note/edit/(\d+)")
class Edit(_handler.LoginBase):
    @staticmethod
    def _can_edit(current_user_id, id):
        if id:
            po = Po.mc_get(id)
            if not po:
                po = None
            if not po.can_admin(current_user_id):
                po = None
        else:
            po = None
        return po or JsDict()

    def get(self, id=0):
        current_user_id = self.current_user_id
        po = self._can_edit(current_user_id, id)
        self.render(po=po, pic_list = pic_list_edit(current_user_id, id))

    def post(self, id=None):
        current_user_id = self.current_user_id
        po = self._can_edit(current_user_id, id)
        name = self.get_argument('name', '')
        txt = self.get_argument('txt', '')
        secret = self.get_argument('secret', None)
        if secret:
            state = STATE_SECRET
        else:
            state = STATE_ACTIVE
        if po:
            if name:
                po.name = name
                po.save()
            if txt:
                po.txt_set(id, txt)
            po_state_set(po, state)
        else:
            po = po_note_new(current_user_id, name, txt, state)
        if po:
            link = po.link
        else:
            link = "/po/note"
        self.redirect(link)










