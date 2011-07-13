#!/usr/bin/env python
# -*- coding: utf-8 -*-
from config import SITE_DOMAIN, SITE_URL
from zweb._handler.main import LoginBase

class Base(LoginBase):
    def prepare(self):
        super(Base, self).prepare()

    def post(self, *arg, **kwds):
        return self.get(*arg, **kwds)
