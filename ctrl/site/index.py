# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.site import urlmap
from zkit.jsdict import JsDict
from zkit.page import page_limit_offset

PAGE_LIMIT = 25


@urlmap('/')
class SiteIndex(LoginBase):
    def get(self):
        pass

    def post(self):
        pass

@urlmap('/new')
class SiteNew(LoginBase):
    def get(self):
        pass

    def post(self):
        pass
