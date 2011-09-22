#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import ZsiteBase, LoginBase, XsrfGetBase
from model.motto import motto
from ctrl._urlmap.zsite import urlmap
from model.zsite_link import link_by_id
from model.cid import CID_USER, CID_SITE
from model.site_po import po_list_by_zsite_id, po_cid_count_by_zsite_id
from zkit.page import page_limit_offset



@urlmap('/')
@urlmap("/-\d+")
class Index(ZsiteBase):
    def get(self, n=1):
        zsite_id = self.zsite_id
        zsite = self.zsite
        user_id = self.current_user_id

        if zsite.cid == CID_SITE:
            total = po_cid_count_by_zsite_id(zsite_id, 0)
            page, limit, offset = page_limit_offset(
                "/-%s",
                total,
                n,
                20
            )
            self.render(
                '/ctrl/zsite/po_view/site_po_page.htm',
                li = po_list_by_zsite_id(user_id, zsite_id, 0, limit, offset),
                page=page,
                total=total
            )
        else:

            self.render(
                motto=motto.get(zsite_id),
            )


@urlmap('/link/(\d+)')
class Link(LoginBase):
    def get(self, id):
        self.redirect(link_by_id(id))




