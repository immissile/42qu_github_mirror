# -*- coding: utf-8 -*-
from config import render
import model._db
from __init__ import Base as _Base, _login_redirect


class Base(_Base):
    def get(self, *args):
        self.redirect('/')

    @property
    def _xsrf(self):
        return '_xsrf=%s'%self.xsrf_token

    def render(self, template_name=None, **kwds):
        kwds['_xsrf'] = self._xsrf
        super(Base, self).render(template_name, **kwds)


class LoginBase(Base):
    def prepare(self):
        super(LoginBase, self).prepare()
        _login_redirect(self)


class XsrfGetBase(LoginBase):
    def prepare(self):
        super(XsrfGetBase, self).prepare()
        self.check_xsrf_cookie()
