#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ctrl._urlmap.zsite import urlmap
from _handler.site import ZsiteBase, _login_redirect
from model.cid import CID_SITE



@urlmap('/mark')
class Mark(LoginBase):
    def get(self):
        zsite_id = self.zsite_id
        current_user_id = self.current_user_id
        can_admin = zsite_user_state(zsite_id, current_user_id)
        if can_admin:
            return self.redirect("/admin")
        self.render()


@urlmap('/about')
class About(SiteBase):
    def get(self):
        self.render()
