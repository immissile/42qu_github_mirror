#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.rss import get_pre_po, PrePo
from zkit.page import page_limit_offset
PAGE_LIMIT = 10
from misc.htm2po.htm2po import htm2po

@urlmap('/rss_index')
@urlmap('/rss_index/(\d+)')
@urlmap('/rss_index/(\d+)-(\-?\d+)')
class RssIndex(Base):
    def get(self,state=0,n=1):
        total = PrePo.where(state=state).count()
        page, limit, offset = page_limit_offset(
                 '/rss_index-%s',
                 total,
                 n,
                 PAGE_LIMIT
                 )
        pre_po = get_pre_po(limit,offset)
        self.render(
                pre_po=pre_po,
                page = page
                )

@urlmap('/rss/(\d+)')
class RssCheck(Base):
    def get(self,id):
        po = PrePo.where(id=id)
        if po:
            htm2po(po.user_id,po.title,po.htm)
        self.redirect('/rss_index')
