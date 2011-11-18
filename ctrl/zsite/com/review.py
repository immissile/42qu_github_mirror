#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ctrl.zsite._handler import ZsiteBase, LoginBase, XsrfGetBase
from ctrl._urlmap.zsite import urlmap
from _handler import AdminBase

@urlmap('/review/admin')
class ReviewAdmin(AdminBase):
    def get(self):
        return self.render()


