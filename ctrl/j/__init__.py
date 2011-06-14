#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ctrl.main import _handler
from model.vote import vote_state
from zweb._urlmap import urlmap
from model.follow import follow_rm, follow_new
from model.po import Po, CID_NOTE
from json import dumps
from zkit.pic import picopen
from model.po_pic import pic_can_add, po_pic_new, po_pic_rm
from model.fs import fs_url_jpg
from model.vote import vote_down_x, vote_down, vote_up_x, vote_up
from model.feed_render import MAXINT, PAGE_LIMIT, render_feed_by_zsite_id, FEED_TUPLE_DEFAULT_LEN
from model.feed import feed_rt, feed_rt_rm, feed_rt_id


@urlmap('/j/rt/(\d+)')
class Rt(_handler.JLoginBase):
    def post(self, id):
        current_user_id = self.current_user_id
        if current_user_id:
            feed_rt(current_user_id, id)
        self.finish("{}")


@urlmap('/j/rt/rm/(\d+)')
class RtRm(_handler.JLoginBase):
    def post(self, id):
        current_user_id = self.current_user_id
        if current_user_id:
            feed_rt_rm(current_user_id, id)
        self.finish("{}")


@urlmap('/j/txt')
class Txt(_handler.Base):
    def get(self):
        self.render()


@urlmap('/j/login')
class Login(_handler.Base):
    def get(self):
        self.render()


