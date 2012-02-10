#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import ZsiteBase, LoginBase, XsrfGetBase
from ctrl._urlmap.zsite import urlmap
from model.cid import CID_SITE
from model.zsite_fav import zsite_fav_get_and_touch
from ctrl.zsite.index import render_zsite_site

@urlmap('/read')
@urlmap('/read-(\d+)')
class Index(LoginBase):
    def get(self, n=1):
        zsite = self.zsite
        if zsite.cid == CID_SITE:
            current_user = self.current_user
            current_user_id = self.current_user_id
            zsite_fav_get_and_touch(zsite, current_user_id)

            li, page = render_zsite_site(self, n, '/read-%s')
            self.render("/ctrl/zsite/site/read.htm", li=li, page=page)
        else:
            self.render()




