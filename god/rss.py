#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.rss import rss_po_list_by_state, RssPo, RSS_UNCHECK, RSS_PRE_PO, RSS_RM
from zkit.page import page_limit_offset
PAGE_LIMIT = 10

@urlmap('/rss_index')
@urlmap('/rss_index/(\d+)')
@urlmap('/rss_index/(\d+)-(\-?\d+)')
class RssIndex(Base):
    def get(self,state=RSS_UNCHECK,n=1):
        total = RssPo.where(state=state).count()
        page, limit, offset = page_limit_offset(
                 '/rss_index/%s-%%s'%state,
                 total,
                 n,
                 PAGE_LIMIT
                 )
        rss_po = rss_po_list_by_state(state,limit,offset)
        self.render(
                rss_po=rss_po,
                page = page
                )
@urlmap('/rss')
@urlmap('/rss/(\d+)/(\d+)')
class RssCheck(Base):
    def get(self,state,id):
        po = RssPo.get(id=id)
        po.state = state
        po.save()
        self.redirect('/rss_index')

    def post(self):
        id = int(self.get_argument('id'))
        txt = self.get_argument('%stxt'%id)
        po = RssPo.get(id=id)
        po.txt = txt
        po.state = RSS_PRE_PO
        po.save()
        self.redirect('/rss_index')


