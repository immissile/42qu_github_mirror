#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.mail_po import STATE_NEW, get_tem_total_by_state, get_tem_by_state, new_mail_tem, rm_tem_by_id, STATE2CN
from zkit.page import page_limit_offset

PAGE_LIMIT = 50

@urlmap('/mail/notify')
@urlmap('/mail/notify/(\d+)')
@urlmap('/mail/notify/(\d+)-(\-?\d+)')
class Index(Base):
    def get(self, state=STATE_NEW, n=1):
        total = get_tem_total_by_state(state)
        page, limit, offset = page_limit_offset(
                '/mail/notify/%s-%%s'%state,
                total,
                n,
                PAGE_LIMIT
                )

        mail_po_list = get_tem_by_state(state, limit, offset)
        self.render(
                mail_po_list=mail_po_list,
                total=total,
                page=page
                )

@urlmap('/mail/notify/rm/(\d+)')
class NotifyRm(Base):
    def get(self, id):
        if id:
            rm_tem_by_id(id)
            self.redirect('/mail/notify')



@urlmap('/mail/notify/add')
class NotifyAdd(Base):
    def get(self):
        self.render()

    def post(self):
        id = self.get_argument('id', None)
        if id:
            new_mail_tem(id)
        self.redirect('/mail/notify')

@urlmap('/mail/group')
class MailGroup(Base):
    def get(self):
        self.render()
