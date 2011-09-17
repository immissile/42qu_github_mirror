#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.zsite import Zsite
from model.cid import CID_USER
from zkit.page import page_limit_offset
from model.zsite_show import user_list_verify, zsite_show_count

PAGE_LIMIT = 100

@urlmap('/user_list')
@urlmap('/user_list-(\d+)')
class Index(Base):
    def get(self, n=1):
        total = Zsite.where().count()
        page, limit, offset = page_limit_offset(
            href='/user_list-%s',
            total=total,
            n=n,
            limit=PAGE_LIMIT
        )
        user_list = Zsite.where().order_by('id desc')[offset:offset+limit]

        self.render(
            user_list=user_list,
            page=page,
        )


@urlmap('/user_list_verify')
@urlmap('/user_list_verify-(\d+)')
class IndexV(Base):
    def get(self, n=1):
        n = int(n)
        count = zsite_show_count(CID_USER)
        page, limit, offset = page_limit_offset('/user_list_verify-%s', count, n, 64)
        zsite_list = Zsite.mc_get_list(user_list_verify(limit, offset))
        self.render(zsite_list=zsite_list, page=page)
