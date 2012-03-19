#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ctrl._urlmap.j import urlmap
from _handler import JLoginBase
from model.site_rec import  site_rec_feeckback
from model.top_rec import top_rec_mark, TOP_REC_CID_OAUTH_BINDED

@urlmap('/j/site/rec/(\d+)-(\d+)')
class SiteRec(JLoginBase):
    def post(self, id, state):
        user_id = self.current_user_id
        site_rec_feeckback(user_id, id, state)
        self.finish('{}')

@urlmap('/j/site/oauth')
class Oauth(JLoginBase):
    def post(self):
        user_id = self.current_user_id
        top_rec_mark(user_id, TOP_REC_CID_OAUTH_BINDED)

@urlmap('/j/site/rec/new')
class SiteRecNew(JLoginBase):
    def post(self):
        self.finish("{}")
        return
