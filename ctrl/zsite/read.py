#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import ZsiteBase, LoginBase, XsrfGetBase
from ctrl._urlmap.zsite import urlmap
from model.cid import CID_SITE
from model.zsite_fav import zsite_fav_get_and_touch
from ctrl.zsite.index import render_zsite_site
from model.rec_read import rec_read_log_by_user_id_auto_more, rec_read_log_count_by_user_id
from tornado.escape import json_encode 
from model.po_json import po_json
#from model.po_tag import po_tag

PAGE_LIMIT = 50

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
#            zsite_id = 137110
#            item_list = po_tag(zsite_id, current_user_id, 15, 0 )
            item_list = []
            po_id_list = rec_read_log_by_user_id_auto_more(
                current_user_id, PAGE_LIMIT/2, 0
            )
            t = [
                0,
                "推荐",
                rec_read_log_count_by_user_id(current_user_id),
                po_json(current_user_id, po_id_list, 47) ,
                1
            ]
            item_list.append(t)


            self.render(
                item_list = json_encode(item_list)
            )








