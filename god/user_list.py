#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.zsite import Zsite
from zkit.page import page_limit_offset
from model.zsite_list import zsite_list_count
from model.zsite_list_0 import user_list_verify

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
        count = zsite_list_count(0, 0)
        page, limit, offset = page_limit_offset('/user_list_verify-%s', count, n, 64)
        zsite_list = Zsite.mc_get_list(user_list_verify(limit, offset))
        self.render(zsite_list=zsite_list, page=page)
