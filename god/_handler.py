#!/usr/bin/env python
#coding:utf-8

from zweb._tornado import web
from config import render
from config import SITE_DOMAIN, SITE_URL
from model.zsite_link import zsite_by_domain
import urlparse
import urllib
import zweb._handler


class Base(zweb._handler.Base):
    def prepare(self):
        if not self.current_user:
            self.redirect(SITE_URL)
        super(Base, self).prepare()

