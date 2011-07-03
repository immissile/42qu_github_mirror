#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import ZsiteBase, LoginBase, XsrfGetBase
from model.motto import motto
from ctrl._urlmap.zsite import urlmap



@urlmap('/')
class Index(ZsiteBase):
    def get(self):
        zsite_id = self.zsite_id
        self.render(
            motto=motto.get(zsite_id)

        )


