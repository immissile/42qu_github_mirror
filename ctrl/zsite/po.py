#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import ZsiteBase, LoginBase, XsrfGetBase, login
from model.zsite_tag import zsite_tag_id_tag_name_by_po_id
from ctrl._urlmap.zsite import urlmap
from model.po import po_rm, po_word_new, Po
from model.po_pos import po_pos_get, po_pos_set
from model import reply
from model.zsite import Zsite
from model.cid import CID_WORD, CID_NOTE, CID_QUESTION, CID_ANSWER


class PoBase(ZsiteBase):
    cid = None

    def get(self, id):
        po = Po.mc_get(id)
        if not po:
            return self.redirect('/')

        if po.user_id != self.zsite_id or po.cid != self.cid:
            link = po.link
            return self.redirect(link)

        user_id = self.current_user_id
        can_admin = po.can_admin(user_id)
        can_view = po.can_view(user_id)
        if can_view and user_id:
            po_pos_set(user_id, po)

        zsite_tag_id, tag_name = zsite_tag_id_tag_name_by_po_id(po.user_id, id)

        return self.render(
            po=po,
            can_admin=can_admin,
            can_view=can_view,
            zsite_tag_id=zsite_tag_id,
            tag_name=tag_name
        )


@urlmap('/word/(\d+)')
class Word(PoBase):
    cid = CID_WORD


@urlmap('/note/(\d+)')
class Note(PoBase):
    cid = CID_NOTE


@urlmap('/question/(\d+)')
class Question(PoBase):
    cid = CID_QUESTION

    @login
    def post(self, id):
        po = Po.mc_get(id)
        if not po or po.cid != self.cid:
            return self.redirect('/')

        if po.user_id != self.zsite_id:
            link = po.link
            return self.redirect(link)

        user_id = self.current_user_id
        if po.can_view(user_id):
            pass


@urlmap('/po/reply/rm/(\d+)')
class ReplyRm(LoginBase):
    def post(self, id):
        user_id = self.current_user_id
        r = reply.Reply.mc_get(id)

        if r:
            po = Po.mc_get(r.rid)
            if po:
                can_rm = r.can_rm(user_id) or po.can_admin(user_id)
                if can_rm:
                    r.rm()

        self.finish({'success': can_rm})


@urlmap('/po/reply/(\d+)')
class Reply(LoginBase):
    def post(self, id):
        po = Po.mc_get(id)
        if po:
            user_id = self.current_user_id
            can_view = po.can_view(user_id)
            link = po.link
            if can_view:
                txt = self.get_argument('txt', '')
                m = po.reply_new(user_id, txt, po.state)
                if m:
                    link = '%s#reply%s' % (link, m)
        else:
            link = '/'
        self.redirect(link)

    def get(self, id):
        po = Po.mc_get(id)
        if po:
            link = po.link
        else:
            link = '/'
        self.redirect(link)


@urlmap('/po/rm/(\d+)')
class Rm(XsrfGetBase):
    def get(self, id):
        user = self.current_user
        user_id = self.current_user_id
        po_rm(user_id, id)
        self.redirect(user.link)

    post = get
