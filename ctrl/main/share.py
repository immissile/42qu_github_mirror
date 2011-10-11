#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import LoginBase
from ctrl._urlmap.main import urlmap
from config import SITE_URL


@urlmap('/share')
class Share(LoginBase):
    def get(self):
        name = self.get_argument('name',None)
        href = self.get_argument('href',None)
        self.render(name=name,href=href)
