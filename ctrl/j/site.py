#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ctrl._urlmap.j import urlmap
from _handler import JLoginBase
from model.cid import CID_SITE
from model.site_rec import  site_rec_feeckback

@urlmap('/j/site/rec/(\d+)-(\d+)')
class SiteRec(JLoginBase):
    def post(self, id, state):
        user_id = self.current_user_id
        site_rec_feeckback(user_id, id, state)
        self.finish('{}')

