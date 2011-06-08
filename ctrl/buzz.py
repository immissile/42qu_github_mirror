#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from zweb._urlmap import urlmap

@urlmap('/buzz')
@urlmap('/buzz/(\d+)')
class Index(LoginBase):
    def get(self, n=1):
        pass
