#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.zsite import Zsite

from zkit.page import page_limit_offset

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

