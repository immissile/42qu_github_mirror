#!/usr/bin/env python
# -*- coding: utf-8 -*-


import _handler
from model.feed import feed_rt, feed_rt_rm, feed_rt_id
from ctrl.j._urlmap import urlmap

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

