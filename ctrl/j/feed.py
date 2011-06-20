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
        self.finish('{}')

@urlmap('/j/feed/up0/(\d+)')
class FeedUpX(JLoginBase):
    def post(self, id):
        current_user_id = self.current_user_id
        vote_up_x(current_user_id, id)
        self.finish('{}')

@urlmap('/j/feed/down1/(\d+)')
class FeedDown(JLoginBase):
    def post(self, id):
        current_user_id = self.current_user_id
        vote_down(current_user_id, id)
        self.finish('{}')

@urlmap('/j/feed/down0/(\d+)')
class FeedDownX(JLoginBase):
    def post(self, id):
        current_user_id = self.current_user_id
        vote_down_x(current_user_id, id)
        self.finish('{}')

@urlmap('/j/feed')
class Feed(JLoginBase):
    def get(self, id=MAXINT):
        current_user_id = self.current_user_id

        result = render_feed_by_zsite_id(current_user_id, PAGE_LIMIT, id)
        for i in result:
            id = i[0]
            i.insert(FEED_TUPLE_DEFAULT_LEN, vote_state(current_user_id, id))
            i.insert(FEED_TUPLE_DEFAULT_LEN, feed_rt_id(current_user_id, id))
        #self.finish(result)
        result = dumps(result)
        result = """
[[107,["zsp007","//80.zuroc.xxx"],[],80,61,0,1308585944,"PO_EN sss",0,0,0],[106,["zsp007","//80.zuroc.xxx"],[],80,61,0,1308585871,"zzzzzzzzzzzzzz",0,0,0],[105,["zsp007","//80.zuroc.xxx"],[],80,61,0,1308585844,"PO_EN",0,0,0],[104,["zsp007","//80.zuroc.xxx"],[],80,61,0,1308585832,"ssssssssssssssssssssss",0,0,0],[103,["zsp007","//80.zuroc.xxx"],[],80,61,0,1308585828,"PO_EN",0,0,0],[102,["zsp007","//80.zuroc.xxx"],[],80,61,0,1308585805,"ssssssssssssss",0,0,0],[101,["zsp007","//80.zuroc.xxx"],[],80,61,0,1308585802,"PO_ENPO_EN",0,0,0],[98,["zsp007","//80.zuroc.xxx"],[],80,61,0,1308585776,"PO_EN",0,0,0],[97,["zsp007","//80.zuroc.xxx"],[],80,61,0,1308585766,"PO_ENPO_ENPO_EN",0,0,0],[96,["zsp007","//80.zuroc.xxx"],[],80,61,0,1308585763,"http://3.zuroc.xxx/",0,0,0],[95,["zsp007","//80.zuroc.xxx"],[],80,63,0,1308585749,"PO_EN",0,0,0],[94,["zsp007","//80.zuroc.xxx"],[],80,62,0,1308585733,"PO_EN",0,0,0,"PO_ENPO_ENPO_ENPO_ENPO_ENPO_ENPO_EN"],[87,["zsp007","//80.zuroc.xxx"],[],80,62,0,1308574197,"** \u6240\u6709\u6587\u7ae0\u7684\u6d4f\u89c8\u9875\u9762",0,0,0,"** 所有文章的浏览页面"]]"""
        self.finish(result)

    post = get
