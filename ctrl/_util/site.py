# -*- coding: utf-8 -*-

from zkit.page import page_limit_offset
from model.zsite_list import zsite_list_active, zsite_list_count_active
from model.zsite_admin import zsite_by_admin_id_count, zsite_list_by_admin_id
from model.cid import CID_SITE

PAGE_LIMIT = 20

class _SiteListBase(object):

    def get(self, n=1):
        total = self._total()
        n = int(n)

        page, limit, offset = page_limit_offset(
            self.page_url,
            total,
            n,
            PAGE_LIMIT,
        )
        page_list = self._page_list(limit, offset)
        return self.render(
            page_list=page_list,
            page=str(page),
            total=total
        )

class FavBase(object):

    def _total(self):
        return zsite_list_count_active(
            self.user_id, CID_SITE
        )

    def _page_list(self, limit, offset):
        return zsite_list_active(
            self.user_id, CID_SITE, limit, offset
        )

class MyBase(object):
    def _total(self):
        return zsite_by_admin_id_count(
            self.user_id
        )

    def _page_list(self, limit, offset):
        return zsite_list_by_admin_id(
            self.user_id, limit, offset
        )
