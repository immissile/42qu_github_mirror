#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import ZsiteBase, LoginBase, XsrfGetBase
from ctrl._urlmap.zsite import urlmap
from model.cid import CID_SITE
from model.zsite_fav import zsite_fav_get_and_touch
from ctrl.zsite.index import render_zsite_site
#from model.po_by_tag import po_by_tag

@urlmap('/read')
@urlmap('/read-(\d+)')
class Index(LoginBase):
    def get(self, n=1):
        zsite = self.zsite
        zsite_id = self.zsite_id
        current_user = self.current_user
        current_user_id = self.current_user_id

        if zsite.cid == CID_SITE:
            zsite_fav_get_and_touch(zsite, current_user_id)
            li, page = render_zsite_site(self, n, '/read-%s')
            self.render("/ctrl/zsite/site/read.htm", li=li, page=page)
        else:
            zsite_id = 137110
            item_list = po_by_tag(zsite_id, current_user_id, 15, 0 )
            self.render(item_list=item_list)




