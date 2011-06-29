#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.zsite import Zsite

@urlmap('/user_list/(\d+)')
class Index(Base):
    def get(self, offset=0, limit=5):
        offset=int(offset)
        if offset < 0:
            offset = 0
        _user_list = Zsite.where().order_by('-id')[offset:offset+limit]
        self.render(
            user_list = _user_list,
            offset = offset,
            limit = limit,
            )
