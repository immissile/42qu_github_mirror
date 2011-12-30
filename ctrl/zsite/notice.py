#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _handler import ZsiteBase, LoginBase, XsrfGetBase, login
from ctrl._urlmap.zsite import urlmap
from zkit.page import page_limit_offset
from model.buzz_at import buzz_at_count,buzz_at_list,buzz_at_pos_set
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

        if n==1:
            if reply_list:
                max_id = reply_list[0][0]
                buzz_at_pos_set(zsite.id,max_id)

        self.render(
            reply_list=reply_list,
            page=page
        )


