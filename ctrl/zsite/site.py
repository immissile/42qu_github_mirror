#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ctrl._urlmap.zsite import urlmap
from _handler import ZsiteBase, LoginBase, XsrfGetBase


@urlmap('/mark')
class Mark(LoginBase):
    def get(self):
        zsite_id = self.zsite_id
        current_user_id = self.current_user_id
        can_admin = zsite_user_state(zsite_id, current_user_id)
        if can_admin:
            return self.redirect("/admin")
        self.render()


