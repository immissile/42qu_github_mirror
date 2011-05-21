#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _handler
from zweb._urlmap import urlmap
from feed import feed_render_iter_for_zsite_follow, PAGE_LIMIT

def _render(,  begin_id=sys.maxint):
    man_id = request.man_id
    if entry_list:
        entry = entry_list[0]
    Man.mc_bind(entry_list, "feed_man", "feed_man_id")
    feed_man_list = tuple(i.feed_man for i in entry_list)
    man_sign_bind(feed_man_list)
    man_ico_url_bind(feed_man_list, "id", "96")


@urlmap("/news")
class News(_handler.LoginBase):
    def get(self):
        begin_id = 0
        current_user_id = current_user.id
        entry_list = feed_render_iter_for_zsite_follow(
            current_user, PAGE_LIMIT, begin_id
        )
        return self.render(
            entry_list = entry_list
        )
