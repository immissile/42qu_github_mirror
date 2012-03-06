#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import ZsiteBase, LoginBase, XsrfGetBase
from model.motto import motto
from ctrl._urlmap.zsite import urlmap
from model.zsite_link import link_by_id
from model.cid import CID_USER, CID_SITE, CID_COM, CID_TAG
from model.site_po import feed_po_list_by_zsite_id, po_cid_count_by_zsite_id, PAGE_LIMIT
from zkit.page import page_limit_offset
from model.zsite_fav import zsite_fav_get_and_touch
from model.rec_read import po_json_by_rec_read
from model.po_tag import tag_cid_count
from zkit.escape import json_encode 
from model.po_tag import REDIS_REC_CID_DICT, po_tag_by_cid 
#from model.po_tag import po_tag

def render_zsite_site(self, n=1, page_template='/-%s'):
    zsite_id = self.zsite_id
    user_id = self.current_user_id

    total = po_cid_count_by_zsite_id(zsite_id, 0)
    page, limit, offset = page_limit_offset(
        page_template,
        total,
        n,
        PAGE_LIMIT
    )
    li = feed_po_list_by_zsite_id(
        user_id, zsite_id, 0, limit, offset
    )
    page = page
    return li, page



@urlmap('/feed')
class Feed(LoginBase):
    def get(self):
        current_user_id = self.current_user_id

#        from model.po_tag import po_tag

        self.render(
            rec_item_list=po_json_by_rec_read( current_user_id)
        )




@urlmap('/')
@urlmap('/-(\d+)')
class Index(ZsiteBase):
    def get(self, n=1):
        zsite_id = self.zsite_id
        zsite = self.zsite
        current_user_id = self.current_user_id

        if zsite.cid == CID_SITE:
            li, page = render_zsite_site(self, n)
            if current_user_id:
                if not zsite_fav_get_and_touch(zsite, current_user_id):
                    return self.redirect('/about')
            self.render(
                '/ctrl/zsite/po_view/site_po_page.htm',
                li=li, page=page
            )
        elif zsite.cid == CID_COM:
            self.render(
                    '/ctrl/com/index/com.htm',
                    user_id=current_user_id
            )
        elif zsite.cid == CID_TAG:
            render_tag_site(self, n)
        else:
            self.render( motto=motto.get(zsite_id) )

@urlmap('/link/(\d+)')
class Link(LoginBase):
    def get(self, id):
        self.redirect(link_by_id(id))


def render_tag_site(self, n=1):
    zsite = self.zsite
    zsite_id = self.zsite_id
    current_user_id = self.current_user_id

    tc = tag_cid_count(zsite_id)

    if len(tc) == 1:
        limit = 12
    else:
        limit = 5 

    tag_cid_json_list = []

    for cid, count in tc:
        if count>limit:
            page = limit
        else:
            page = 0

        t = [
cid, 
REDIS_REC_CID_DICT[cid],
count, 
po_tag_by_cid(cid, zsite_id, current_user_id, limit),
page
        ]
        
        tag_cid_json_list.append(t)


    self.render(
        '/ctrl/zsite/index/tag.htm',
        tag_cid_json_list = json_encode(tag_cid_json_list)
    )
#    zsite = self.zsite
#    zsite_id = zsite.id
#    page, limit, offset = page_limit_offset(
#        '/-%s', total, n, limit=15
#    )
#    current_user_id = self.current_user_id
#    item_list = po_tag(zsite_id, current_user_id, limit, offset )
#    self.render(
#        template,
#        page=str(page),
#        total=total,
#        item_list=item_list,
#    )


