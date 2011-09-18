#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import ZsiteBase, LoginBase, XsrfGetBase
from model.motto import motto
from ctrl._urlmap.zsite import urlmap
from model.zsite_link import link_by_id
from model.cid import CID_USER, CID_SITE


ZSITE_INDEX_TEMPLATE = {
    CID_USER: 'user',
    CID_SITE: 'site',
}


@urlmap('/')
class Index(ZsiteBase):
    def get(self):
        zsite_id = self.zsite_id
        zsite = self.zsite
        self.render(
            "ctrl/zsite/index/%s.htm"%ZSITE_INDEX_TEMPLATE[zsite.cid],
            motto=motto.get(zsite_id),
        )




@urlmap('/link/(\d+)')
class Link(LoginBase):
    def get(self, id):
        self.redirect(link_by_id(id))




