#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from zweb._urlmap import urlmap
from model.notice import notice_list, notice_count, notice_unread
from zkit.page import page_limit_offset

PAGE_LIMIT = 100

@urlmap('/notice')
@urlmap('/notice-(\d+)')
class Page(LoginBase):
    def get(self, n=1):
        user_id = self.current_user_id
        total = notice_count(user_id)
        page, limit, offset = page_limit_offset(
            '/notice-%s',
            total,
            n,
            PAGE_LIMIT
        )
        if type(n) == str and offset >= total:
            return self.redirect('/notice')
        unread = notice_unread.get(user_id)
        if unread:
            notice_unread.set(user_id, 0)
        self.render(
            notice_list=notice_list(user_id, limit, offset),
            page=page,
        )
