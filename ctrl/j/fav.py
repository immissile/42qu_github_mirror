#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _handler import JLoginBase
from model.zsite_url import zsite_by_domain
from model.zsite_fav import zsite_fav_new

@urlmap('/j/fav')
class Fav(JLoginBase):
    def get(self):
        current_user = self.current_user
        current_user_id = self.current_user_id

        host = self.request.host
        zsite = zsite_by_domain(host)

        if zsite and zsite.cid in (CID_SITE, CID_COM):
            zsite_fav_new(zsite, current_user_id)
        

        txt = self.get_argument('txt', None)
        if txt:
            from model.reply import STATE_ACTIVE
            zsite.reply_new(current_user, txt, STATE_ACTIVE)


        self.finish('{}')

