#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import ZsiteBase, LoginBase, XsrfGetBase
from ctrl._urlmap.zsite import urlmap

@urlmap('/')
class Index(ZsiteBase):
    def get(self):
        self.render()
