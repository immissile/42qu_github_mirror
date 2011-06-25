#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import JLoginBase
from ctrl._urlmap.j import urlmap
from model.vote import vote_state
from model.po import Po, CID_NOTE
from yajl import dumps
from model.vote import vote_down_x, vote_down, vote_up_x, vote_up
from model.feed_render import MAXINT, PAGE_LIMIT, render_feed_by_zsite_id, FEED_TUPLE_DEFAULT_LEN
from model.feed import feed_rt, feed_rt_rm, feed_rt_id


@urlmap('/j/feed/up1/(\d+)')
class FeedUp(JLoginBase):
    def post(self, id):
        current_user_id = self.current_user_id
        vote_up(current_user_id, id)
        feed_rt(current_user_id, id)
        self.finish('{}')

@urlmap('/j/feed/up0/(\d+)')
class FeedUpX(JLoginBase):
    def post(self, id):
        current_user_id = self.current_user_id
        vote_up_x(current_user_id, id)
        feed_rt_rm(current_user_id, id)
        self.finish('{}')

@urlmap('/j/feed/down1/(\d+)')
class FeedDown(JLoginBase):
    def post(self, id):
        current_user_id = self.current_user_id
        vote_down(current_user_id, id)
        feed_rt_rm(current_user_id, id)
        self.finish('{}')

@urlmap('/j/feed/down0/(\d+)')
class FeedDownX(JLoginBase):
    def post(self, id):
        current_user_id = self.current_user_id
        vote_down_x(current_user_id, id)
        self.finish('{}')

@urlmap('/j/feed/(\d+)')
class Feed(JLoginBase):
    def get(self, id):
        id = int(id)
        if id == 0:
            id = MAXINT
        current_user_id = self.current_user_id

        result = render_feed_by_zsite_id(current_user_id, PAGE_LIMIT, id)
        for i in result:
            id = i[0]
            i.insert(FEED_TUPLE_DEFAULT_LEN, vote_state(current_user_id, id))
            #i.insert(FEED_TUPLE_DEFAULT_LEN, feed_rt_id(current_user_id, id))
        #self.finish(result)
        result = dumps(result)
        self.finish(result)

    post = get


