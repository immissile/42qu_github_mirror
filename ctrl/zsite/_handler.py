#!/usr/bin/env python
# -*- coding: utf-8 -*-
from config import render
from config import SITE_DOMAIN, SITE_URL
from model.zsite_link import zsite_by_domain
from zweb._handler import Base as _Base, _login_redirect, login

class Base(_Base):
    def get(self):
        self.redirect('/')

    def prepare(self):
        host = self.request.host
        zsite = zsite_by_domain(host)
        if zsite is None:
            self.zsite_id = 0
        else:
            self.zsite_id = zsite.id
        self.zsite = zsite
        super(Base, self).prepare()

    @property
    def _xsrf(self):
        return '_xsrf=%s'%self.xsrf_token

    def render(self, template_name=None, **kwds):
        kwds['_xsrf'] = self._xsrf
        kwds['zsite_id'] = self.zsite_id
        kwds['zsite'] = self.zsite
        super(Base, self).render(template_name, **kwds)

class ZsiteBase(Base):
    def prepare(self):
        super(ZsiteBase, self).prepare()
        if self.zsite_id == 0:
            current_user = self.current_user
            if current_user:
                link = "%s/%s"%(current_user.link, path)
            else:
                link = SITE_URL
            return self.redirect(link)

class JLoginBase(Base):
    def prepare(self):
        super(JLoginBase, self).prepare()
        if not self.current_user:
            self.finish({'login': 1})

class LoginBase(ZsiteBase):
    def prepare(self):
        super(LoginBase, self).prepare()
        _login_redirect(self)

class XsrfGetBase(LoginBase):
    def prepare(self):
        super(XsrfGetBase, self).prepare()
        self.check_xsrf_cookie()
