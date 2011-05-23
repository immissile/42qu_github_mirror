#!/usr/bin/env python
#coding:utf-8

import _handler
from zweb._urlmap import urlmap
from model.mblog import Mblog, mblog_note_can_view, mblog_rm,\
        mblog_note_new, STATE_SECRET, STATE_ACTIVE, mblog_state_set
from model.zsite import Zsite
from zkit.jsdict import JsDict
from model.txt import txt_new

@urlmap("/note/(\d+)")
class Index(_handler.Base):
    def get(self, id):
        mblog = Mblog.get(id)
        current_user_id = self.current_user_id
        if mblog.user_id != self.zsite_id:
            zsite = Zsite.mc_get(mblog.user_id)
            return self.redirect(
                "%s/note/%s"%(
                    zsite.link,
                    id
                ), True
            )
        can_view = mblog_note_can_view(mblog, current_user_id)
        return self.render(
            mblog=mblog,
            can_view=can_view
        )


@urlmap("/note/(\d+)/rm")
class Rm(_handler.XsrfGetBase):
    def get(self, id):
        current_user = self.current_user
        current_user_id = self.current_user_id
        mblog_rm(current_user_id, id)
        self.redirect(current_user.link)

    post = get

def can_edit(current_user_id, id):
    if id:
        mblog = Mblog.mc_get(id)
        if not mblog:
            mblog = None
        if not mblog.can_admin(current_user_id):
            mblog = None
    else:
        mblog = None
    return mblog or JsDict()

@urlmap("/po/note")
@urlmap("/note/(\d+)/edit")
class Edit(_handler.LoginBase):
    def get(self, id=None):
        current_user_id = self.current_user_id
        mblog = can_edit(current_user_id, id)
        self.render(mblog=mblog)

    def post(self, id=None):
        current_user_id = self.current_user_id
        mblog = can_edit(current_user_id, id)
        name = self.get_argument('name', '')
        txt = self.get_argument('txt', '')
        secret = self.get_argument('secret', None)
        if secret:
            state = STATE_SECRET
        else:
            state = STATE_ACTIVE
        if mblog:
            if name:
                mblog.name = name
                mblog.save()
            if txt:
                txt_new(id, txt)
            mblog_state_set(mblog, state)
        else:
            mblog = mblog_note_new(current_user_id, name, txt, state)
        self.redirect(mblog.link)










