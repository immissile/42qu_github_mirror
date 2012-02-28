#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ctrl._urlmap.j import urlmap
from _handler import JLoginZsiteBase
from model.cid import CID_TAG
from zkit.page import page_limit_offset, Page
from json import dumps
from model.po_tag import po_tag_by_cid, tag_cid_count 

PAGE_LIMIT = 1 

@urlmap('/j/tag/(\d+)-(\-?\d+)')
class TagMore(JLoginZsiteBase):
    def get(self, cid, n):
        zsite_id = self.zsite_id        
        current_user_id = self.current_user_id

        page, limit, offset = page_limit_offset(
            'javascript:tag_cid_page(%s,%%s)'%cid,
            int(tag_cid_count(zsite_id, cid) or 0),
            n,
            PAGE_LIMIT
        )
        page = str(page) or 0
        print int(tag_cid_count(zsite_id, cid) or 0)
 
        self.finish({
'li':po_tag_by_cid(cid, zsite_id, current_user_id, limit, offset),
'page':page

        })



