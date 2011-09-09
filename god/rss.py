#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.rss import get_pre_po, PrePo, RSS_UNCHECK, RSS_PRE_PO, RSS_RM
from zkit.page import page_limit_offset
PAGE_LIMIT = 10

@urlmap('/rss_index')
@urlmap('/rss_index/(\d+)')
@urlmap('/rss_index/(\d+)-(\-?\d+)')
class RssIndex(Base):
    def get(self,state=RSS_UNCHECK,n=1):
        total = PrePo.where(state=state).count()
        page, limit, offset = page_limit_offset(
                 '/rss_index-%s',
                 total,
                 n,
                 PAGE_LIMIT
                 )
        pre_po = get_pre_po(state,limit,offset)
        self.render(
                pre_po=pre_po,
                page = page
                )

@urlmap('/rss/(\d+)/(\d+)')
class RssCheck(Base):
    def get(self,state,id):
        po = PrePo.get(id=id)
        po.state = state
        po.save()
        self.redirect('/rss_index')
