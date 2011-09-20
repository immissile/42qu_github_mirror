#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.rss import rss_po_list_by_state, RssPo, RSS_UNCHECK, RSS_PRE_PO, RSS_RM, rss_po_total, get_rss_by_gid, rss_total_gid
from zkit.page import page_limit_offset

PAGE_LIMIT = 10

@urlmap('/rss_index')
@urlmap('/rss_index/(\d+)')
@urlmap('/rss_index/(\d+)-(\-?\d+)')
class RssIndex(Base):
    def get(self, state=RSS_UNCHECK, n=1):
        total = rss_po_total(state)

        page, limit, offset = page_limit_offset(
                 '/rss_index/%s-%%s'%state,
                 total,
                 n,
                 PAGE_LIMIT
             )
        rss_po_list = rss_po_list_by_state(state, limit, offset)
        self.render(
                rss_po_list=rss_po_list,
                page=page
            )

@urlmap('/rss_gid/(\d+)')
@urlmap('/rss_gid/(\d+)-(\-?\d+)')
class RssGid(Base):
    def get(self, gid=0,n=1):
        gid = int(gid)
        total = rss_total_gid(gid)
        page, limit, offset = page_limit_offset(
                '/rss_gid/%s-%%s'%gid,
                total,
                n,
                PAGE_LIMIT
                )
        rss_list = get_rss_by_gid(gid, limit, offset)
        self.render(
                rss = rss_list,
                page = page
                )

@urlmap('/rss_gid/edit/(\d+)')
class RssEdit(Base):
    def post(self, id):
        id=int(id)
        rss = Rss.get(id=id)
        rss.gid = rss.gid-1
        rss.save()

        self.redirect('/rss_gid/%s'%rss.gid)

@urlmap('/rss/edit/(\d+)')
class RssEdit(Base):
    def post(self, id):
        id=int(id)
        txt = self.get_argument('txt')

        po = RssPo.get(id=id)
        po.txt = txt
        po.state = RSS_PRE_PO
        po.save()

        self.finish('')
