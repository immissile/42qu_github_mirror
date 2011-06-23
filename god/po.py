#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.zsite import Zsite, ZSITE_STATE_WAIT_VERIFY, zsite_verify_yes, zsite_verify_no
from model.user_mail import mail_by_user_id
from model.mail import sendmail
from model.cid import CID_PO, CID_WORD, CID_NOTE, CID_QUESTION
from model.po import Po
from model.po_show import po_show_new, po_show_count, po_show_list
from model.state import STATE_DEL, STATE_SECRET, STATE_ACTIVE
from zkit.page import page_limit_offset

PAGE_LIMIT = 50

@urlmap('/po(?:-(\d+))?')
class PoList(Base):
    def get(self, n=1):
        qs = Po.where('state>%s', STATE_DEL)
        total = qs.count()
        page, limit, offset = page_limit_offset(
            '/po-%s',
            total,
            n,
            PAGE_LIMIT,
        )
        li = qs.order_by('id desc')[offset: offset + limit]
        Po.mc_bind(li, 'question', 'rid')
        self.render(
            po_list=li,
            page=page,
        )


@urlmap('/po/show(?:-(\d+))?')
class PoShow(Base):
    def get(self, n):
        page, limit, offset = page_limit_offset(
            '/po/show-%s',
            po_show_count(0),
            n,
            PAGE_LIMIT,
        )
        li = po_show_list(0, 'id', limit, offset)
        self.render(
            po_list=li,
            page=page,
        )


@urlmap('/po/add_show/(\d+)')
class PoAddShow(Base):
    def get(self, id):
        next = self.request.headers.get('Referer', '')
        po = Po.mc_get(id)
        if po:
            self.render(
                po=po,
                next=next,
            )

    def post(self, id):
        po = Po.mc_get(id)
        cid = self.get_argument('cid', None)
        next = self.get_argument('next', '/po')
        if po and cid:
            po_show_new(po, cid)
            return self.redirect(next)
        self.render(
            po=po,
            next=next,
        )
