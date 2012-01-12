# -*- coding: utf-8 -*-

from _handler import Base, LoginBase
from ctrl._urlmap.tag import urlmap
from zkit.page import page_limit_offset


@urlmap('/')
class Index(Base):
    def get(self):
        page, limit, offset = page_limit_offset(

        )
        self.render()


