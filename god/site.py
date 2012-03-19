#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from zkit.page import page_limit_offset
from model.zsite_site import site_id_list_by_state, site_count_by_state, ZSITE_STATE_SITE_PUBLIC
from model.cid import CID_SITE
from model.zsite_show import zsite_show_rm, zsite_show_new
from model.zsite import Zsite

PAGE_LIMIT = 20

@urlmap('/site')
@urlmap('/site/(\d+)')
@urlmap('/site/(\d+)-(\-?\d+)')
class Index(Base):
    def get(self, state=0, n=1):
        state = int(state)
        total = site_count_by_state(state)

        page, limit, offset = page_limit_offset(
            '/site/%s-%%s'%state,
            total,
            n,
            PAGE_LIMIT
        )

        site_id_list = site_id_list_by_state(state, limit, offset)
        self.render(
            site_id_list=site_id_list,
            page=page
        )


@urlmap('/site/show/new/(\d+)')
class SiteAddShow(Base):
    def get(self, id):
        zsite_show_new(id, CID_SITE)
        self.redirect('/site')

@urlmap('/site/show/rm/(\d+)')
class SiteRmShow(Base):
    def get(self, id):
        zsite = Zsite.mc_get(id)
        zsite_show_rm(zsite)
        self.redirect('/site')
