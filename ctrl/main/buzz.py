#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl.main._urlmap import urlmap
from zkit.page import page_limit_offset
from model.buzz import buzz_list as _buzz_list, buzz_count

PAGE_LIMIT = 100

@urlmap('/buzz')
@urlmap('/buzz/(\d+)')
class Page(LoginBase):
    def get(self, n=1):
        user_id = self.current_user_id
        n = int(n)
        page, limit, offset = page_limit_offset(
            '/buzz/%s',
            buzz_count(user_id),
            n,
            PAGE_LIMIT
        )
        buzz_list = _buzz_list(user_id, limit, offset)
        if n > 1 and not buzz_list:
            return self.redirect('/buzz')
        self.render(
            buzz_list=buzz_list,
            page=page,
        )
