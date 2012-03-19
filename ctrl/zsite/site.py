#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ctrl._urlmap.zsite import urlmap
from model.motto import motto_get
from _handler_site import SiteBase, LoginBase, XsrfGetBase, AdminBase
from model.zsite_site import site_can_admin
from zkit.jsdict import JsDict
from model.zsite_link import link_list_cid_by_zsite_id, SITE_LINK_ZSITE_DICT, link_list_save
from model.ico import site_ico_bind
from model.motto import motto_set
from model.txt import txt_get, txt_new
from model.ico import ico96
from ctrl.site.index import _site_save
from model.zsite_url import url_by_id, url_new
from model.zsite_fav import zsite_fav_rm
from model.search_zsite import search_new
from _handler import ZsiteBase
from model.zsite_list import zsite_list_count, zsite_id_list
from ctrl._util.site import _SiteListBase, FavBase, MyBase
from model.cid import CID_SITE
from zkit.page import page_limit_offset
from model.zsite import Zsite
from model.zsite_fav import zsite_fav_get_and_touch
from model.wall import Wall, wall_by_from_id_to_id
from model.reply import Reply
from ctrl.zsite.index import render_zsite_site

PAGE_LIMIT = 56

@urlmap('/admin')
class Admin(AdminBase):
    def get(self):
        zsite = self.zsite
        zsite_id = self.zsite_id
        link_list , link_cid = link_list_cid_by_zsite_id(zsite_id, SITE_LINK_ZSITE_DICT)
        self.render(
            errtip=JsDict(),
            link_cid=link_cid,
            link_list=link_list,
            name=zsite.name,
            motto=motto_get(zsite_id),
            txt=txt_get(zsite_id),
            pic_id=ico96.get(zsite_id)
        )


    _site_save = _site_save

    def post(self):
        errtip, link_cid, link_kv, name, motto, url, txt, pic_id = self._site_save()
        current_user_id = self.current_user_id
        zsite_id = self.zsite_id
        zsite = self.zsite

        success = False

        if not errtip:
            success = True
            if not url_by_id(zsite_id) and url:
                url_new(zsite_id, url)
            zsite.name = name
            zsite.save()

            link_list_save(zsite_id, link_cid, link_kv)
            txt_new(zsite_id, txt)
            motto_set(zsite_id, motto)
            site_ico_bind(current_user_id, pic_id, zsite_id)
            search_new(zsite_id)

        self.render(
            success=success,
            errtip=errtip,
            link_cid=link_cid,
            link_list=link_kv,
            name=name,
            motto=motto,
            txt=txt,
            pic_id=pic_id,
            url=url
        )


@urlmap('/admin/review')
class AdminReview(LoginBase):
    def get(self):
        self.render()

@urlmap('/mark/rm')
class MarkRm(XsrfGetBase):
    def get(self):
        zsite = self.zsite
        current_user_id = self.current_user_id
        zsite_fav_rm(zsite, current_user_id)
        return self.redirect(zsite.link)




@urlmap('/mark')
class Mark(LoginBase):
    def get(self):
        zsite_id = self.zsite_id
        current_user_id = self.current_user_id

        can_admin = site_can_admin(zsite_id, current_user_id)

        if can_admin:
            return self.redirect('/admin')
        wall = wall_by_from_id_to_id(current_user_id, zsite_id)
        if wall:
            reply_last = wall.reply_last()
            if reply_last:
                self.render(reply=reply_last)

        self.render()


    def post(self):
        zsite = self.zsite
        current_user = self.current_user
        zsite_id = self.zsite_id
        current_user_id = self.current_user_id
        txt = self.get_argument('txt', None)

        if txt:
            wall = wall_by_from_id_to_id(current_user_id, zsite_id)
            if wall:
                reply_last = wall.reply_last()
            else:
                reply_last = None

            if reply_last:
                reply_last.txt_set(txt)
            else:
                zsite = self.zsite
                from model.reply import STATE_ACTIVE
                zsite.reply_new(current_user, txt, STATE_ACTIVE)
        self.get()


@urlmap('/about')
class About(SiteBase):
    def get(self):
        li, page = render_zsite_site(self, 1)
        self.render(
            li=li, page=page
        )

@urlmap('/site')
class Site(ZsiteBase):
    def get(self):
        return self.render()


class SiteListBase(_SiteListBase):
    template = '/ctrl/zsite/site/site_list.htm'

    @property
    def user_id(self):
        return self.zsite_id

@urlmap('/site/fav')
@urlmap('/site/fav-(\d+)')
class FavSite( SiteListBase, FavBase, ZsiteBase):
    page_url = '/site/fav-%s'


@urlmap('/site/my')
@urlmap('/site/my-(\d+)')
class MySite( SiteListBase, MyBase, ZsiteBase):
    page_url = '/site/my-%s'


