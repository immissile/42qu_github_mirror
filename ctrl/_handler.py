#!/usr/bin/env python
# -*- coding: utf-8 -*-

from zweb._tornado import web
from config import render
from config import SITE_DOMAIN, SITE_URL
from model.zsite_link import zsite_by_domain
import urlparse
import urllib
import zweb._handler

class Base(zweb._handler.Base):
    def prepare(self):
        host = self.request.host
        zsite = zsite_by_domain(host)
        self.zsite = zsite
        if zsite is None and host != SITE_DOMAIN:
            return self.redirect(SITE_URL)

class LoginBase(Base):
    def prepare(self):
        if not self.current_user:
            url = self.get_login_url()
            if "?" not in url:
                if urlparse.urlsplit(url).scheme:
                    # if login url is absolute, make next absolute too
                    next_url = self.request.full_url()
                else:
                    next_url = self.request.uri
                url += "?" + urllib.urlencode(dict(next=next_url))
            self.redirect(url)
            return
        super(LoginBase,self).prepare()
