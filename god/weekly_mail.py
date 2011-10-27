#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from zkit.page import page_limit_offset
from model.weekly_mail import weekly_mail_new, weekly_mail_list_limit, weekly_mail_total, weekly_mail_rm, WeeklyMail,weekly_mail_update
from zkit.page import page_limit_offset

PAGE_LIMIT = 20

@urlmap('/weekly/mail')
@urlmap('/weekly/mail/(\d+)')
class Po(Base):
    def get(self, id=0):
        if id:
            wm = WeeklyMail.get(id)
        else:
            wm = None

        self.render(wm = wm)

    def post(self, id=0):
        title = self.get_argument('title', None)
        txt = self.get_argument('txt', None)
        if id:
            state = int(self.get_argument('state', None)) 
            weekly_mail_update(id,title,txt,state)
            return self.redirect('/weekly/mail-1')
        else:
            wm = weekly_mail_new(title, txt)


@urlmap('/weekly/mail-(\d+)')
class Page(Base):
    def get(self, n=1):
        n = int(n)
        total = weekly_mail_total()
        page, limit, offset = page_limit_offset(
                '/weekly/mail-%s',
                total,
                n,
                PAGE_LIMIT
                )
        wm_list = weekly_mail_list_limit(limit, offset)
        self.render(
                wm_list=wm_list,
                page=page
        )

@urlmap('/weekly_mail/rm/(\d+)')
class WeeklyMailRm(Base):
    def get(self, id):
        weekly_mail_rm(id)
        self.redirect('/weekly/mail-1')

