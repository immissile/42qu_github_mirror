#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.zsite import urlmap

@urlmap('/live')
class Index(LoginBase):
    def get(self):
        site_rec = self.current_user 
        return self.render(site_rec=site_rec)
