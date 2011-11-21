#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ctrl.zsite._handler import ZsiteBase, LoginBase, XsrfGetBase
from ctrl._urlmap.zsite import urlmap
from _handler import AdminBase
from model.zsite_member import zsite_member_can_admin

@urlmap('/review/admin')
class ReviewAdmin(AdminBase):
    def get(self):
        zsite_id = self.zsite_id
        current_user_id = self.current_user_id
        can_admin = zsite_member_can_admin(zsite_id, current_user_id)
        return self.render(can_admin=can_admin)

@urlmap('/review/invite')
class ReviewInvite(LoginBase):
    def get(self):
        return self.render()

@urlmap('/review')
class Review(LoginBase):
    def get(self):
        zsite_id = self.zsite_id
        current_user_id = self.current_user_id
        can_admin = zsite_member_can_admin(zsite_id, current_user_id)
        current_user_id = self.current_user_id
        self.render(can_admin=can_admin)


@urlmap('/review-(\d+)')
class ReviewPage(ZsiteBase):
    def get(self, n):
        zsite_id = self.zsite_id
        current_user_id = self.current_user_id
        can_admin = zsite_member_can_admin(zsite_id, current_user_id)
        if can_admin:
            return self.redirect("/review/admin")
        self.render(can_admin=can_admin)
        
