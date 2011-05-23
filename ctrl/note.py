#!/usr/bin/env python
#coding:utf-8

import _handler
from zweb._urlmap import urlmap
from model.mblog import Mblog, mblog_note_can_view, mblog_rm
from model.zsite import Zsite
from zkit.jsdict import JsDict

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
    mblog = Mblog.mc_get(id)
    if not mblog:
        self.redirect("/")
        return
    if not mblog.can_admin(current_user_id):
        self.redirect(mblog.link)
        return
    return mblog

@urlmap("/cout/note")
@urlmap("/note/(\d+)/edit")
class Edit(_handler.LoginBase):
    def get(self, id=None):
        if id:
            mblog = can_edit(self.current_user_id, id)
        else:
            mblog = JsDict()
        self.render(
            mblog=mblog
        )

    def post(self, id=None):
        if id:
            mblog = can_edit(current_user_id, id)

        self.redirect(mblog.link)

#@urlmap("/cout/note")
#class Note(_handler.LoginBase):
#    def get(self, id=None):
#        return self.render("/ctrl/note/edit.htm")
#
#    def post(self, id=None):
#        current_user = self.current_user
#        current_user_id = current_user.id
#        name = self.get_argument('name', '')
#        txt = self.get_argument('txt', '')
#        secret = self.get_argument('secret', None)
#        if secret:
#            state = MBLOG_STATE_SECRET
#        else:
#            state = MBLOG_STATE_ACTIVE
#        m = mblog_note_new(current_user_id, name, txt, state)
#        if m:
#            return self.redirect("/note/%s"%m.id)
#









