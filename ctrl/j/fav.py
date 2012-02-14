#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ctrl._urlmap.j import urlmap
from _handler import JLoginBase
from model.zsite_url import zsite_by_domain
from model.zsite_fav import zsite_fav_new, zsite_fav_rm
from model.cid import CID_SITE, CID_COM, CID_TAG

@urlmap('/j/fav/rm')
class FavRm(JLoginBase):
    def post(self):
        current_user = self.current_user
        current_user_id = self.current_user_id

        host = self.request.host
        zsite = zsite_by_domain(host)

        if zsite and zsite.cid in (CID_SITE, CID_COM, CID_TAG):
            zsite_fav_rm(zsite, current_user_id)

        self.finish('{}')

@urlmap('/j/fav')
class Fav(JLoginBase):
    def get(self):
        current_user = self.current_user
        current_user_id = self.current_user_id

        host = self.request.host
        zsite = zsite_by_domain(host)
        zsite_id = zsite.id
        cid = zsite.cid

        if zsite and cid in (CID_SITE, CID_COM, CID_TAG):
            zsite_fav_new(zsite, current_user_id)

        txt = self.get_argument('txt', None)
        if txt:
            if cid == CID_SITE:
                from model.reply import STATE_ACTIVE
                zsite.reply_new(current_user, txt, STATE_ACTIVE)
            elif cid == CID_COM:
                from model.po_review import po_review_new
                po_review_new(zsite_id, current_user_id, name)

        self.finish('{}')

