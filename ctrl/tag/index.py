# -*- coding: utf-8 -*-

from _handler import Base, LoginBase
from ctrl._urlmap.tag import urlmap
from zkit.page import page_limit_offset

@urlmap('/log')
class Log(LoginBase):
    def get(self):
        self.render('/ctrl/zsite/tag/log.htm')
