#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _handler
from zweb._urlmap import urlmap

@urlmap("/")
class Index(_handler.Base):
    def get(self):
        self.render()

@urlmap("/follow")
class Follow(_handler.XsrfGetBase):
    def get(self):
        self.render()
