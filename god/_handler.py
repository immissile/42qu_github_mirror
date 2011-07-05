#!/usr/bin/env python
# -*- coding: utf-8 -*-
from config import SITE_DOMAIN, SITE_URL
import zweb._handler

class Base(zweb._handler.Base):
    def prepare(self):
        super(Base, self).prepare()

    def post(self, *arg, **kwds):
        return self.get(*arg, **kwds)
