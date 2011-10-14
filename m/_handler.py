# -*- coding: utf-8 -*-
from config import render
import model._db
from zweb._handler import Base as _Base, login
from zweb._handler.main import XsrfGetBase, Base as BaseBase
from model.zsite import Zsite
from config import render, SITE_DOMAIN, SITE_URL
from model.oauth2 import oauth_access_token_verify
from zweb._handler.main import LoginBase as _LoginBase
from model.user_auth import mail_password_verify
import urllib
import urlparse


def post(self, *args, **kwds):
    return self.get(*args, **kwds)

class Base(BaseBase):
    def get(self, *args):
        self.redirect(self.request.host)

def _login_redirect(self):
    if self._finished:
        return
    if not self.current_user:
        url = self.get_login_url()
        if '?' not in url:
            if urlparse.urlsplit(url).scheme:
                # if login url is absolute, make next absolute too
                next_url = self.request.full_url()
            else:
                next_url = self.request.uri
            request = self.request
            host = request.host
            if host != SITE_DOMAIN and next_url.startswith('/') and not next_url.startswith('//'):
                next_url = '//%s%s'%(host, next_url)
            url += '?' + urllib.urlencode(dict(next=next_url))
        self.redirect('/login')
        return True

class LoginBase(Base):
    def prepare(self):
        super(LoginBase, self).prepare()
        _login_redirect(self)

