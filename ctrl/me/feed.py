# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from _urlmap import urlmap
from model.feed_render import render_feed_by_zsite_id
from model.feed import PAGE_LIMIT, MAXINT

@urlmap('/feed')
class Index(LoginBase):
    def get(self):
        begin_id = MAXINT
        current_user = self.current_user
        current_user_id = current_user.id
        entry_list = render_feed_by_zsite_id(
            current_user_id, PAGE_LIMIT, begin_id
        )
        return self.render(
            entry_list=entry_list
        )
