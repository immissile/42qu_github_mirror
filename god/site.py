#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from zkit.page import page_limit_offset
from model.zsite_site import site_by_state, site_state_total, ZSITE_STATE_SITE_SECRET, ZSITE_STATE_SITE_PUBLIC
from model.cid import CID_SITE
from model.zsite_show import zsite_show_rm, zsite_show_new

PAGE_LIMIT = 20

@urlmap('/site')
@urlmap('/site/(\d+)')
@urlmap('/site/(\d+)-(\-?\d+)')
class Index(Base):
    def get(self,state=0,n=1):
        state=int(state)
        total = site_state_total(state)
        page,limit,offset = page_limit_offset(
                '/site/%s-%%s'%state,
                total,
                n,
                PAGE_LIMIT
                )
        site_id_list = site_by_state(state,limit,offset)
        self.render(
                site_id_list=site_id_list,
                page=page
                )


@urlmap('/site/add_show/(\d+)')
class SiteAddShow(Base):
    def get(self,id):
        if id:
            zsite_show_new(id,CID_SITE)
        self.redirect('/site')

@urlmap('/site/rm_show/(\d+)')
class SiteRmShow(Base):
    def get(self,id):
        if id:
            zsite_show_rm(id,CID_SITE)
        self.redirect('/site')
