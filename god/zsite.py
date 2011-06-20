#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.zsite import Zsite
from model.zsite_list_0 import zsite_show_new, zsite_show_rm
from model.zsite_link import url_new
from model.user_mail import mail_by_user_id
from model.mail import sendmail

@urlmap('/zsite/(\d+)')
class Index(Base):
    def get(self, id):
        zsite = Zsite.mc_get(id)
        self.render(zsite=zsite)

@urlmap('/zsite/show/(\d+)')
class Show(Base):
    def get(self, id):
        zsite = Zsite.mc_get(id)
        if zsite:
            zsite_show_new(id)
        self.redirect('/zsite/%s'%id)

@urlmap('/zsite/show/rm/(\d+)')
class ShowRm(Base):
    def get(self, id):
        zsite_show_rm(id)
        self.redirect('/zsite/%s'%id)

@urlmap('/zsite/mail/(\d+)')
class Mail(Base):
    def get(self, id):
        zsite = Zsite.mc_get(id)
        self.render(zsite=zsite)

    def post(self, id):
        zsite = Zsite.mc_get(id)
        title = self.get_argument('title', '')
        txt = self.get_argument('txt', '')
        if zsite and title and txt:
            mail = mail_by_user_id(id)
            name = zsite.name
            sendmail(title, txt, mail, name)
        self.redirect('/zsite/%s' % id)
