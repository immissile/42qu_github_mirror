#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ctrl._urlmap.j import urlmap
from _handler import JLoginZsiteBase
from model.cid import CID_TAG
from zkit.page import limit_offset
from json import dumps
from model.po_tag import po_tag_by_cid, tag_cid_count 

PAGE_LIMIT = 12

@urlmap('/j/tag/(\d+)-(\-?\d+)')
class TagMore(JLoginZsiteBase):
    def get(self, cid, n):

        n, limit, offset = limit_offset(n, PAGE_LIMIT)
        zsite_id = self.zsite_id        
        current_user_id = self.current_user_id
 
        self.finish({
            'n':n,
            'li':po_tag_by_cid(cid, zsite_id, current_user_id, limit, offset),
            'count':tag_cid_count(zsite_id, cid)
        })



