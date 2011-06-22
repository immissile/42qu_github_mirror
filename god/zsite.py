#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.zsite import Zsite, ZSITE_STATE_WAIT_VERIFY, zsite_verify_yes, zsite_verify_no
from model.zsite_list_0 import zsite_show_new, zsite_show_rm
from model.zsite_link import url_new
from model.user_mail import mail_by_user_id
from model.mail import sendmail
from model.cid import CID_ZSITE
from zkit.page import page_limit_offset


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


@urlmap('/zsite/verify/(0|1)/(\d+)')
class Verify(Base):
    def post(self, state, id):
        state = int(state)
        txt = self.get_argument('txt', '')
        zsite = Zsite.mc_get(id)
        if zsite and zsite.state == ZSITE_STATE_WAIT_VERIFY:
            if state:
                zsite_verify_yes(zsite)
            else:
                zsite_verify_no(zsite, txt)
            self.finish({'state': True})
        else:
            self.finish({'state': False})

PAGE_LIMIT = 100

#@urlmap('/zsite/verify(%s)(?:-(\d+))?' % '|'.join(map(str, CID_ZSITE)))
@urlmap('/zsite/verify(%s)' % '|'.join(map(str, CID_ZSITE)))
class VerifyList(Base):
    def get(self, cid):
        qs = Zsite.where(cid=cid, state=ZSITE_STATE_WAIT_VERIFY)
        total = qs.count()
        li = qs.order_by('id')[:PAGE_LIMIT]
        extra = total - len(li)
        self.render(
            zsite_list=li,
            total=total,
            extra=extra,
        )
