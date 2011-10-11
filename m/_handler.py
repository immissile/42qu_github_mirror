# -*- coding: utf-8 -*-
from config import render
import model._db
from zweb._handler import Base as _Base, BaseBase, _login_redirect, login
from model.zsite import Zsite
from model.oauth2 import oauth_access_token_verify
from zweb._handler.main import LoginBase as _LoginBase
from model.user_auth import mail_password_verify


def post(self, *args, **kwds):
    return self.get(*args, **kwds)

class Base(_Base):
    def get(self, *args):
        self.redirect('/')

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
        self.redirect(url)
        return True

class LoginBase(_LoginBase):
    def prepare(self):
        super(LoginBase, self).prepare()
        _login_redirect(self)

