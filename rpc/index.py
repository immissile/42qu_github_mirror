#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from config import SITE_URL

@urlmap('/')
class Index(Base):
    def get(self):
        self.redirect(SITE_URL)
