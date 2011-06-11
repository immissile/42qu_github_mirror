#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _handler
from zweb._urlmap import urlmap
from model.feed_merge import feed_render_iter_by_follow
from model.feed import PAGE_LIMIT, MAXINT

@urlmap('/feed')
class Index(_handler.LoginBase):
    def get(self):
        begin_id = MAXINT
        current_user = self.current_user
        current_user_id = current_user.id
        entry_list = feed_render_iter_by_follow(
            current_user_id, PAGE_LIMIT, begin_id
        )
        return self.render(
            entry_list=entry_list
        )
