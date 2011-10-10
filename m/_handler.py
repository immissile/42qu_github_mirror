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
