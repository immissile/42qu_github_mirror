#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import JLoginBase
from model.feed import feed_rt, feed_rt_rm, feed_rt_id
from ctrl._urlmap.j import urlmap

@urlmap('/j/rt/(\d+)')
class Rt(JLoginBase):
    def post(self, id):
        current_user_id = self.current_user_id
        if current_user_id:
            feed_rt(current_user_id, id)
        self.finish('{}')


@urlmap('/j/rt/rm/(\d+)')
class RtRm(JLoginBase):
    def post(self, id):
        current_user_id = self.current_user_id
        if current_user_id:
            feed_rt_rm(current_user_id, id)
        self.finish('{}')
