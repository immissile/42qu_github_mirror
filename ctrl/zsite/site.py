#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ctrl._urlmap.zsite import urlmap
from model.motto import motto_get
from _handler_site import SiteBase, LoginBase
from model.zsite_admin import admin_id_list_by_zsite_id, zsite_user_state
from zkit.jsdict import JsDict
from model.zsite_link import link_list_cid_by_zsite_id,SITE_LINK_ZSITE_DICT
from model.txt import txt_get

@urlmap('/admin')
class Admin(LoginBase):
    def get(self):
        zsite = self.zsite
        zsite_id = self.zsite_id 
        link_list , link_cid = link_list_cid_by_zsite_id(zsite_id, SITE_LINK_ZSITE_DICT)
        self.render(
            errtip=JsDict(),
            link_cid=link_cid,
            link_list=link_list,
            name = zsite.name,
            motto = motto_get(zsite_id),
            txt = txt_get(zsite_id)
        )


@urlmap('/mark')
class Mark(LoginBase):
    def get(self):
        zsite_id = self.zsite_id
        current_user_id = self.current_user_id
        can_admin = zsite_user_state(zsite_id, current_user_id)
        if can_admin:
            return self.redirect("/admin")
        self.render()


@urlmap('/about')
class About(SiteBase):
    def get(self):
        self.render()

