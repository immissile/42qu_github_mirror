#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base, JLoginBase
import _handler
from ctrl._urlmap.j import urlmap
from zkit.errtip import Errtip
from model.follow import follow_rm, follow_new
from model.zsite import Zsite

@urlmap('/j/login')
class Login(Base):
    def get(self):
        self.render(errtip=Errtip())

@urlmap('/follow/(\d+)')
class Follow(JLoginBase):
    def get(self, id):
        current_user_id = self.current_user_id

        zsite = Zsite.mc_get(id)
        if zsite:
            follow_new(current_user_id, id)

@urlmap('/follow/rm/(\d+)')
class FollowRm(JLoginBase):
    def get(self, id):
        current_user_id = self.current_user_id

        zsite = Zsite.mc_get(id)
        if zsite:
            follow_rm(current_user_id, id)

