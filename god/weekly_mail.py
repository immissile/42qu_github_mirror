#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from zkit.page import page_limit_offset
from model.weekly_mail import weekly_mail_new, get_weekly_mail_list, weekly_mail_total, get_weekly_mail_list_limit,weekly_mail_remove, Weekly_mail,weekly_mail_update
from zkit.page import page_limit_offset
PAGE_LIMIT = 10

@urlmap('/weekly_mail/new')
class Weekly_mailNew(Base):
    def get(self):
        self.render('/god/weekly_mail/new.htm')
    def post(self):
        title = self.get_argument('title', None)
        txt = self.get_argument('txt', None)
        wm = weekly_mail_new(title, txt)

@urlmap('/weekly_mail/(\d+)')
class Weekly_mail_(Base):
    def get(self, n=1):
        n = int(n)
        total = weekly_mail_total()
        page, limit, offset = page_limit_offset(
                '/weekly_mail/%s',
                total,
                n,
                PAGE_LIMIT
                )
        wm_list = get_weekly_mail_list_limit(limit, offset)
        self.render(
                wm_list=wm_list,
                page=page
                )

@urlmap('/weekly_mail/rm/(\d+)')
class Weekly_mailRm(Base):
    def get(self, id):
        weekly_mail_remove(id)
        self.redirect('/weekly_mail/1')

@urlmap('/weekly_mail/edit/(\d+)')
class Weekly_mailEdit(Base):
    def get(self, id):
        wm = Weekly_mail.get(id)
        self.render(wm=wm)
    def post(self,id):
        id = int(id)
        title = self.get_argument('title', None)
        txt = self.get_argument('txt', None)
        state = int(self.get_argument('state', None)) 
        weekly_mail_update(id,title,txt,state)
        self.redirect('/weekly_mail/1')
