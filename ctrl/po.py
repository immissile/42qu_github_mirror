#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _handler
from zweb._urlmap import urlmap
from model.po import po_word_new,Po
from model import reply
from model.zsite import Zsite


class IndexBase(_handler.Base):
    def po(self, id):
        po = Po.mc_get(id)
        current_user_id = self.current_user_id
        if not po:
            return self.redirect("/")
        if po.user_id != self.zsite_id:
            zsite = Zsite.mc_get(po.user_id)
            return self.redirect(
                "%s%s"%(zsite.link, po.link), True
            )
        return po


@urlmap("/note/(\d+)", template="ctrl/note/index.htm")
@urlmap("/word/(\d+)", template="ctrl/word/index.htm")
class Index(IndexBase):
    def initialize(self, template):
        self.template = template

    def get(self, id):
        po = self.po(id)
        current_user_id = self.current_user_id
        if po:
            can_view = po.can_view(current_user_id)
            return self.render(
                po=po,
                can_view=can_view
            )

@urlmap("/po/(\d+)")
class PoIndex(IndexBase):
    def get(self, id):
        po = self.po(id)
        if po:
            return self.redirect(po.link)

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



@urlmap("/po/rm/(\d+)")
class Rm(_handler.XsrfGetBase):
    def get(self, id):
        current_user = self.current_user
        current_user_id = self.current_user_id
        po_rm(current_user_id, id)
        self.redirect(current_user.link)

    post = get

