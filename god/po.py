#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.zsite import Zsite, ZSITE_STATE_WAIT_VERIFY, zsite_verify_yes, zsite_verify_no, zsite_new
from model.user_mail import mail_by_user_id
from model.mail import sendmail
from model.cid import CID_PO, CID_WORD, CID_NOTE, CID_QUESTION, CID_CHANNEL
from model.po import Po, po_state_set
from model.po_show import po_show_new, po_show_count, po_show_list, po_show_rm
from model.state import STATE_DEL, STATE_SECRET, STATE_ACTIVE, STATE_PO_ZSITE_SHOW_THEN_REVIEW
from zkit.page import page_limit_offset
from model.god_po_show import mc_po_show_zsite_channel

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


@urlmap('/po/state/(\d+)/(%s|%s)' % (STATE_SECRET, STATE_ACTIVE))
class PoState(Base):
    def post(self, id, state):
        po = Po.mc_get(id)
        state = int(state)
        if po:
            po_state_set(po, state)
        self.finish('{}')


@urlmap('/po/show(?:-(\d+))?')
class PoShow(Base):
    template = '/god/po/po_list.htm'

    def get(self, n):
        page, limit, offset = page_limit_offset(
            '/po/show-%s',
            po_show_count(),
            n,
            PAGE_LIMIT,
        )
        li = po_show_list(0, 'id', limit, offset)
        self.render(
            po_list=li,
            page=page,
        )

@urlmap('/po/show/rm/(\d+)')
class PoShowRm(Base):
    def get(self, id):
        po_show_rm(id)
        self.redirect("/po/show/set/%s"%id)

@urlmap('/po/show/set/(\d+)')
class PoShowSet(Base):
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
        next = self.get_argument('next', '/po')
        broad = self.get_argument('broad',None)
        site = self.get_argument('site',None)

        if po:
            if broad:
                po_show_new(po)

            if site:
                po.zsite_id = int(site)
                po.state = STATE_PO_ZSITE_SHOW_THEN_REVIEW
                po.save()

            return self.redirect(next)

        self.render(
            po=po,
            next=next,
        )

