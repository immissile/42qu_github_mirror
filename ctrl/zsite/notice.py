#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _handler import ZsiteBase, LoginBase, XsrfGetBase, login
from ctrl._urlmap.zsite import urlmap
from zkit.page import page_limit_offset
from model.buzz_at import buzz_at_count,buzz_at_list,buzz_at_pos
from model.zsite import Zsite
from model.cid import CID_SITE

PAGE_LIMIT = 42
@urlmap('/notice/buzz/at')
@urlmap('/notice/buzz/at-(\-?\d+)')
class At(ZsiteBase):
    def get(self, n=1):
        zsite = self.zsite
        zsite_url = zsite.link
        total =  buzz_at_count(zsite.id)

        page, limit, offset = page_limit_offset(
            '%s/notice/buzz/at-%%s' % zsite_url,
            total,
            n,
            PAGE_LIMIT
        )

        reply_list = buzz_at_list(zsite.id,limit,offset)

        self.render(
            reply_list=reply_list,
            page=page
        )

