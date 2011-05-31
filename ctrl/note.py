#!/usr/bin/env python
#coding:utf-8

import _handler
from zweb._urlmap import urlmap
from model.po import Po, po_rm,\
        po_note_new, STATE_SECRET, STATE_ACTIVE, po_state_set, CID_NOTE
from model import reply
from model.zsite import Zsite
from zkit.jsdict import JsDict
from model.txt import txt_new
from json import dumps

@urlmap("/po/(\d+)")
class Index(_handler.Base):
    def get(self, id):
        po = Po.mc_get(id)
        current_user_id = self.current_user_id
        if not po or po.cid != CID_NOTE:
            return self.redirect("/")
        if po.user_id != self.zsite_id:
            zsite = Zsite.mc_get(po.user_id)
            return self.redirect(
                "%s/po/%s"%(
                    zsite.link,
                    id
                ), True
            )
        can_view = po.can_view(current_user_id)
        return self.render(
            po=po,
            can_view=can_view
        )




@urlmap("/po/note")
@urlmap("/po/edit/(\d+)")
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

    def get(self, id=None):
        current_user_id = self.current_user_id
        po = self._can_edit(current_user_id, id)
        self.render(po=po)

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
                txt_new(id, txt)
            po_state_set(po, state)
        else:
            po = po_note_new(current_user_id, name, txt, state)
        if po:
            link = po.link
        else:
            link = "/po/note"
        self.redirect(link)










