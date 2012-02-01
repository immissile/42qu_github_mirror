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
from model.po_by_tag import po_by_tag,zsite_tag_po_count

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


#@urlmap('/live')
#class Live(ZsiteBase):
#    def get(self):
#        self.redirect("/feed", True)

@urlmap('/feed')
class Feed(LoginBase):
    def get(self):
        current_user_id = self.current_user_id

#        from model.po_by_tag import po_by_tag
 
        self.render(
            rec_item_list = po_json_by_rec_read(
                current_user_id
            )
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
            render_tag_site(self,n)
        else:
            self.render( motto=motto.get(zsite_id) )


@urlmap('/link/(\d+)')
class Link(LoginBase):
    def get(self, id):
        self.redirect(link_by_id(id))


def render_tag_site(self,n=1,template='/ctrl/tag/index/index.htm'):
    total = zsite_tag_po_count(self.zsite.id)
    page, limit, offset = page_limit_offset(
        "/-%s", total, n, limit = 15
    )
    current_user_id = self.current_user_id
    items = po_by_tag(self.zsite.id, current_user_id, limit, offset )
    self.render(
        template,
        page  = str(page),
        total = total,
        items = items,
    )


