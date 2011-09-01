#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import ZsiteBase, LoginBase, XsrfGetBase
from model.motto import motto
from ctrl._urlmap.zsite import urlmap
from model.zsite_link import link_by_id
from model.cid import CID_USER, CID_SITE
from model.zsite_admin import admin_id_list_by_zsite_id


ZSITE_INDEX_TEMPLATE = {
    CID_USER: 'ctrl/zsite/index/index.htm',
    CID_SITE: 'ctrl/zsite/index/site.htm',
}


@urlmap('/')
class Index(ZsiteBase):
    def get(self):
        zsite_id = self.zsite_id
        self.render(
            ZSITE_INDEX_TEMPLATE.get(self.zsite.cid),
            motto=motto.get(zsite_id),
        )


@urlmap('/link/(\d+)')
class Link(LoginBase):
    def get(self, id):
        self.redirect(link_by_id(id))


@urlmap('/rm')
class SiteRm(LoginBase):
    def get(self):
        zsite = self.zsite
        zsite_id = self.zsite_id
        current_user_id = self.current_user_id
        if zsite.cid == CID_SITE and current_user_id in admin_id_list_by_zsite_id(zsite_id):
            zsite_rm_site(zsite_id)
            self.finish('解散成功')
        else:
            self.finish('解散失败')
