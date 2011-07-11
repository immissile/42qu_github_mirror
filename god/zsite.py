#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
from _handler import Base
from _urlmap import urlmap
from model.zsite import Zsite, ZSITE_STATE_WAIT_VERIFY, zsite_verify_yes, zsite_verify_no
from model.zsite_list_0 import zsite_show_new, zsite_show_rm
from model.zsite_url import url_new
from model.user_mail import mail_by_user_id
from model.mail import sendmail
from model.cid import CID_ZSITE
from zkit.page import page_limit_offset

from model.txt import txt_get, txt_new
from model.motto import motto as _motto
from model.user_mail import user_id_by_mail
from model.zsite_url import id_by_url
from model.user_session import user_session

@urlmap('/zsite/(\d+)')
class Index(Base):
    def get(self, id):
        zsite = Zsite.mc_get(id)
        if zsite:
            txt = txt_get(id)
            self.render(txt=txt, zsite=zsite)
        else:
            self.redirect('/')


    def post(self, id):
        zsite = Zsite.mc_get(id)

        name = self.get_argument('name', None)
        motto = self.get_argument('motto', None)
        txt = self.get_argument('txt', '')

        if name:
            zsite.name = name
            zsite.save()

        if motto:
            _motto.set(id, motto)

        if txt:
            txt_new(id, txt)

        self.redirect('/zsite/%s' % id)


@urlmap('/zsite/show/(\d+)')
class Show(Base):
    def get(self, id):
        zsite = Zsite.mc_get(id)
        rank = self.get_argument('rank', 0)
        rank = int(rank)
        if zsite:
            zsite_show_new(id, rank)
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

##########
from config import SITE_DOMAIN
from urlparse import urlparse
from model.zsite_url import id_by_url
from model.zsite import Zsite
from model.user_mail import user_id_by_mail

def zsite_by_query(query):
    user_id = None

    if '@' in query:
        user_id = user_id_by_mail(query)
    elif SITE_DOMAIN in query:
        key = urlparse(query).netloc.split('.', 1)[0]
        user_id = id_by_url(key)
    elif query.isdigit():
        if Zsite.mc_get(query):
            user_id = query
    else:
        user_id = id_by_url(query)
    return user_id


@urlmap('/zsite/user_search')
class UserSearch(Base):
    def get(self):
        self.render(
            input='',
        )

    def post(self):
        query = self.get_argument('input', None)
        query = urllib.unquote(query).strip()

        user_id = zsite_by_query(query)
        if user_id:
            url = '/zsite/%s' % user_id
            return self.redirect(url)
        else:
            self.render(input=query)

@urlmap('/zsite/avatar/(\d+)')
class avatar(Base):
    def get(self, avatar_id):
        session = user_session(avatar_id)
        self.set_cookie('s', session)
        current_user = Zsite.mc_get(avatar_id)
        self.redirect(current_user.link)
