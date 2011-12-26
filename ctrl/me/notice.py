# -*- coding: utf-8 -*-
from _handler import LoginBase
from ctrl._urlmap.me import urlmap
from model.buzz import Buzz as _Buzz,buzz_set_read
from model.notice import notice_list, notice_count, notice_unread, Notice as N
from model.state import STATE_APPLY,STATE_BUZZ_ACTIVE, STATE_BUZZ_RM
from zkit.page import page_limit_offset
from model.buzz import buzz_list, buzz_count

PAGE_LIMIT = 20

@urlmap('/notice/resume')
class Resume(LoginBase):
    def get(self):
        self.render()

@urlmap('/notice/?')
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


@urlmap('/notice/(\d+)')
class Notice(LoginBase):
    def get(self, id):
        user_id = self.current_user_id
        n = N.mc_get(id)
        if n and n.to_id == user_id and n.state >= STATE_APPLY:
            link = n.link_to
            n.read(user_id)
            if link:
                return self.redirect(link)
        return self.redirect('/notice')

