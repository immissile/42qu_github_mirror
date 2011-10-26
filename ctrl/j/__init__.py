#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base, JLoginBase
import _handler
from ctrl._urlmap.j import urlmap
from zkit.errtip import Errtip
from model.follow import follow_rm, follow_new
from model.zsite import Zsite
from model.zsite import user_can_reply
from ctrl.zsite.wall import post_reply
from model.buzz import mq_buzz_follow_new

@urlmap('/j/login')
class Login(Base):
    def get(self):
        self.render(errtip=Errtip())

@urlmap('/j/follow/(\d+)')
class Follow(JLoginBase):
    def get(self, id):
        current_user_id = self.current_user_id

        zsite = Zsite.mc_get(id)

        if zsite:
            follow_new(current_user_id, id)
            mq_buzz_follow_new(current_user_id, id)

@urlmap('/j/follow/reply/(\d+)')
class FollowRm(JLoginBase):
    def get(self, id):
        current_user = self.current_user
        if not user_can_reply(current_user):
            self.finish('{"can_not_reply":1}')
        else:
            zsite = Zsite.mc_get(id)
            if zsite:
                post_reply(self, zsite.reply_new)
            self.finish('{}')


@urlmap('/j/follow/rm/(\d+)')
class FollowRm(JLoginBase):
    def get(self, id):
        current_user_id = self.current_user_id

        zsite = Zsite.mc_get(id)
        if zsite:
            follow_rm(current_user_id, id)

        self.finish('{}')
