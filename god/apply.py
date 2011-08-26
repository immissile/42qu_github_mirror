#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from zkit.page import page_limit_offset
from model.oauth2 import OauthClient

PAGE_LIMIT = 50

@urlmap('/apply_list')
@urlmap('/apply_list-(\d+)')
class ApplyList(Base):
    def get(self, n=1):
        total = OauthClient.where().count()
        page, limit, offset = page_limit_offset(
            href='/apply_list-%s',
            total=total,
            n=n,
            limit=PAGE_LIMIT
        )
        apply_list = OauthClient.where().order_by('id desc')[offset:offset+limit]

        self.render(
            apply_list=apply_list,
            page=page,
        )


