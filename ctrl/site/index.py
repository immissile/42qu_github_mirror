# -*- coding: utf-8 -*-

from _handler import Base
from ctrl._urlmap.site import urlmap
from zkit.jsdict import JsDict
from zkit.page import page_limit_offset

PAGE_LIMIT = 25


@urlmap('/')
class Index(Base):
    def get(self):
        return self.render()

@urlmap('/new')
class New(Base):
    def get(self):
        return self.render()





