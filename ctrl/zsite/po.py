#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import ZsiteBase, LoginBase, XsrfGetBase, login
from model.zsite_tag import zsite_tag_id_tag_name_by_po_id
from ctrl._urlmap.zsite import urlmap
from model.po import po_rm, po_word_new, Po, STATE_SECRET, STATE_ACTIVE
from model.po_question import po_answer_new
from model.po_pos import po_pos_get, po_pos_set
from model import reply
from model.zsite import Zsite
from model.zsite_tag import zsite_tag_list_by_zsite_id_with_init, tag_id_by_po_id, zsite_tag_new_by_tag_id, zsite_tag_new_by_tag_name, zsite_tag_rm_by_tag_id, zsite_tag_rename
from model.cid import CID_WORD, CID_NOTE, CID_QUESTION


class PoBase(ZsiteBase):
    cid = None

    def po(self, id):
        po = Po.mc_get(id)
        if po:
            if po.user_id == self.zsite_id and po.cid == self.cid:
                return po
            return self.redirect(po.link)
        return self.redirect('/')

    def get(self, id):
        po = self.po(id)
        if po is None:
            return

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
            tag_name=tag_name,
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
        question = self.po(id)
        if question is None:
            return

        user_id = self.current_user_id
        if not question.can_view(user_id):
            return self.get(id)

        name = self.get_argument('name', '')
        txt = self.get_argument('txt', '')
        if not (name or txt):
            return self.get(id)

        secret = self.get_argument('secret', None)
        arguments = self.request.arguments
        if secret:
            state = STATE_SECRET
        else:
            state = STATE_ACTIVE

        name = name or '回复%s' % question.name
        po = po_answer_new(user_id, id, name, txt, state)

        if po:
            if po.cid == CID_NOTE:
                answer_id = po.id
                link = '/po/tag/%s' % answer_id
                zsite_tag_new_by_tag_id(po)
#                update_pic(arguments, user_id, po_id, 0)
#                mc_pic_id_list.delete('%s_%s' % (user_id, 0))
            else:
                link = '%s#answer%s' % (question.link, po.id)
        else:
            link = '%s#answer' % question.link
        self.redirect(link)


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
