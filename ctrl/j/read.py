#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ctrl._urlmap.j import urlmap
from model.rec_read import rec_read_log_by_user_id, rec_read_log_count_by_user_id
from model.po_json import po_json

PAGE_LIMIT = 12 

@urlmap('/j/read/(\d+)-(\-?\d+)')
class Read(JLoginZsiteBase):
    def get(self, tag_id, n):
        zsite_id = self.zsite_id
        current_user_id = self.current_user_id

        tag_id = int(tag_id)
        if tag_id == 0:
            count = rec_read_log_count_by_user_id(current_user_id)
            id_list_getter = lambda limit, offset: rec_read_log_by_user_id(current_user_id, limit, offset)

        page, limit, offset = page_limit_offset(
            'javascript:tag_cid_page(%s,%%s)'%cid,
            count,
            n,
            PAGE_LIMIT
        )
        li = id_list_getter(limit, offset)
        page = str(page) or 0
        self.finish({
            'li':po_json(current_user_id, li, 47),
            'page':page
        })

