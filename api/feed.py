#!/usr/bin/env python
#coding:utf-8
import _handler
from _urlmap import urlmap
from model.feed_api_render import render_feed_api_by_zsite_id, PAGE_LIMIT
from yajl import dumps


@urlmap('/user/live')
class UserFeed(_handler.OauthBase):
    def get(self, id=MAXINT):
        user_id = int(self.get_argument('user_id'))
        li, begin_id = render_feed_by_zsite_id(user_id, PAGE_LIMIT, id)
        self.finish({
            'items': li,
            'begin_id': begin_id,
        })
