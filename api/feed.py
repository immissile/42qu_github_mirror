#!/usr/bin/env python
#coding:utf-8
from _handler import OauthBase, OauthAccessBase
from _urlmap import urlmap
from model.feed_api_render import render_feed_api_by_zsite_id, render_user_feed_api_by_zsite_id, PAGE_LIMIT

PAGE_LIMIT = 10


@urlmap('/live')
class Feed(OauthAccessBase):
    def get(self):
        user_id = self.current_user_id
        begin_id = self.get_argument('begin_id', None)
        if begin_id:
            begin_id = int(begin_id)
        li, begin_id = render_feed_api_by_zsite_id(user_id, PAGE_LIMIT, begin_id)
        self.finish({
            'items': li,
            'begin_id': begin_id,
        })


@urlmap('/user/live')
class UserFeed(OauthBase):
    def get(self):
        user_id = int(self.get_argument('user_id'))
        begin_id = self.get_argument('begin_id', None)
        if begin_id:
            begin_id = int(begin_id)
        li, begin_id = render_user_feed_api_by_zsite_id(user_id, PAGE_LIMIT, begin_id)
        self.finish({
            'items': li,
            'begin_id': begin_id,
        })
