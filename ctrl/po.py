#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _handler
from zweb._urlmap import urlmap
from model.po import po_word_new
from model import reply



@urlmap("/po/word")
class Word(_handler.LoginBase):
    def post(self):
        current_user = self.current_user
        txt = self.get_argument('txt', '')
        if txt.strip():
            po_word_new(current_user.id, txt)
        return self.redirect("/feed")


@urlmap("/po/reply/rm/(\d+)")
class ReplyRm(_handler.LoginBase):
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


@urlmap("/po/reply/(\d+)")
class Reply(_handler.LoginBase):
    def post(self, id):
        po = Po.mc_get(id)
        if po:
            current_user_id = self.current_user_id
            can_view = po.can_view(current_user_id)
            link = None
            if can_view:
                txt = self.get_argument('txt', '')
                m = po.reply_new(current_user_id, txt, po.state)
                if m:
                    link = "%s#reply%s"%(po.link, m)
            if link is None:
                link = po.link
        else:
            link = "/"
        self.redirect(link)


    def get(self, id):
        po = Po.mc_get(id)
        if po:
            link = po.link
        else:
            link = "/"
        self.redirect(link)



