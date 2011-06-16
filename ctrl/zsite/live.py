#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.zsite import urlmap
from model.feed_render import render_feed_by_zsite_id
from model.feed import PAGE_LIMIT, MAXINT

@urlmap('/live')
class Index(Base):
    def get(self):
        begin_id = MAXINT
        zsite = self.zsite
        zsite_id = zsite.id
        entry_list = render_feed_by_zsite_id(
            zsite_id, PAGE_LIMIT, begin_id
        )
        return self.render(
            entry_list=entry_list
        )
