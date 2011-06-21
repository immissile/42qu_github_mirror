#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap

from model.cid import CID_ICO, CID_ICO96, CID_PO_PIC, CID_PIC
from model.pic import Pic, pic_list_to_review_by_cid, pic_to_review_count_by_cid, pic_list_reviewed_by_cid_state, pic_yes, pic_no, pic_reviewed_count_by_cid
from model.zsite import Zsite

CID_PIC = '|'.join(map(str, (CID_ICO, CID_PO_PIC)))

PAGE_LIMIT = 16

@urlmap('/pic/review(%s)' % CID_PIC)
class Review(Base):
    def get(self, cid):
        pic_list = pic_list_to_review_by_cid(int(cid), PAGE_LIMIT)
        Zsite.mc_bind(pic_list, 'user', 'user_id')
        self.render(
            pic_list=pic_list,
            total=pic_to_review_count_by_cid(cid),
        )

    def post(self):
        current_user_id = self.current_user_id
        id_list_all = self.get_arguments('pic_all')
        id_list = set(self.get_arguments('pic_yes'))
        for i in id_list_all:
            if i in id_list:
                pic_yes(i, current_user_id)
            else:
                pic_no(i, current_user_id)
        self.redirect(self.request.path)


@urlmap('/pic/reviewed(%s)/(0|1)' % CID_PIC)
@urlmap('/pic/reviewed(%s)/(0|1)-(\d+)' % CID_PIC)
class Reviewed(Base):
    def get(self, cid, state, n=1):
        path_base = self.request.path.split('-', 1)[0]
        total = pic_reviewed_count_by_cid(cid, state)
        page, limit, offset = page_limit_offset(
            '%s-%%s' % path_base,
            total,
            n,
            PAGE_LIMIT,
        )
        if type(n) == str and offset >= total:
            return self.redirect(path_base)
        pic_list = pic_list_reviewed_by_cid_state(cid, state)
        Zsite.mc_bind(pic_list, 'user', 'user_id')
        self.render(
            pic_list=pic_list,
            page=page,
        )
