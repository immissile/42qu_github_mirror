#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from zweb._urlmap import urlmap
from zkit.page import page_limit_offset
from model.buzz import buzz_list, buzz_count

PAGE_LIMIT = 100

@urlmap('/buzz')
@urlmap('/buzz/(\d+)')
class Page(LoginBase):
    def get(self, n=1):
        user_id = self.current_user_id
        page, limit, offset = page_limit_offset(
            '/buzz/%s',
            buzz_count(user_id),
            n,
            PAGE_LIMIT
        )
        self.render(
            buzz_list=buzz_list(user_id, limit, offset),
            page=page,
        )
