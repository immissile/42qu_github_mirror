#!/usr/bin/env python
#coding:utf-8

import _handler
from zweb._urlmap import urlmap
from model.po import Po, po_note_can_view, po_rm,\
        po_note_new, STATE_SECRET, STATE_ACTIVE, po_state_set
from model import reply
from model.zsite import Zsite
from zkit.jsdict import JsDict
from model.txt import txt_new
from json import dumps

@urlmap("/note/(\d+)")
class Index(_handler.Base):
    def get(self, id):
        po = Po.mc_get(id)
        current_user_id = self.current_user_id
        if po.user_id != self.zsite_id:
            zsite = Zsite.mc_get(po.user_id)
            return self.redirect(
                "%s/note/%s"%(
                    zsite.link,
                    id
                ), True
            )
        can_view = po_note_can_view(po, current_user_id)
        return self.render(
            po=po,
            can_view=can_view
        )


@urlmap("/note/reply/rm/(\d+)")
class ReplyRm(_handler.XsrfGetBase):
    def post(self, id):
        current_user_id = self.current_user_id
        r = reply.Reply.mc_get(id)
        can_rm = r.can_rm(current_user_id)

        if r:
            po = Po.mc_get(r.rid)
            if po:
                if can_rm is False and po.can_admin(current_user_id):
                    can_rm = True

        if can_rm:
            r.rm()

        self.finish(dumps({'success' : can_rm}))

@urlmap("/note/reply/(\d+)")
class Reply(_handler.LoginBase):
    def post(self, id):
        po = Po.mc_get(id)
        current_user_id = self.current_user_id
        can_view = po_note_can_view(po, current_user_id)
        link = None
        if can_view:
            txt = self.get_argument('txt', '')
            m = po.reply_new(current_user_id, txt, po.state)
            if m:
                link = "/note/%s#reply%s"%(id, m)
        if link is None:
            link = po.link
        self.redirect(link)


    def get(self, id):
        po = Po.mc_get(id)
        self.redirect(po.link)

@urlmap("/note/rm/(\d+)")
class Rm(_handler.XsrfGetBase):
    def get(self, id):
        current_user = self.current_user
        current_user_id = self.current_user_id
        po_rm(current_user_id, id)
        self.redirect(current_user.link)

    post = get


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










