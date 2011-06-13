#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _handler
from zweb._urlmap import urlmap
from model.follow import follow_rm, follow_new


@urlmap('/follow')
class Follow(_handler.XsrfGetBase):
    def get(self):
        current_user = self.current_user
        zsite = self.zsite
        follow_new(current_user.id, zsite.id)
        self.render()

@urlmap('/follow/rm')
class FollowRm(_handler.XsrfGetBase):
    def get(self):
        current_user = self.current_user
        zsite = self.zsite
        follow_rm(current_user.id, zsite.id)
        self.redirect('/')
