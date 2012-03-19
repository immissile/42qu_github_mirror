#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap

from model.cid import CID_ICO, CID_ICO96, CID_PO_PIC
from model.pic import pic_yes, pic_no
from model.pic_review import pic_to_review_count_by_cid, pic_list_to_review_by_cid, pic_list_reviewed_by_cid_state, pic_reviewed_count_by_cid_state
from model.zsite import Zsite
from zkit.page import page_limit_offset

CID_PIC = '|'.join(map(str, (CID_ICO, CID_PO_PIC)))

PAGE_LIMIT = 64

@urlmap('/pic/review(%s)' % CID_PIC)
class Review(Base):
    def get(self, cid):
        cid = int(cid)
        pic_list = pic_list_to_review_by_cid(cid, PAGE_LIMIT)

        if not pic_list:
            self.redirect('/zsite/verify/uncheck')

        Zsite.mc_bind(pic_list, 'user', 'user_id')
        self.render(
            cid=cid,
            pic_list=pic_list,
            total=pic_to_review_count_by_cid(cid),
        )

    def post(self, cid):
        current_user_id = self.current_user_id

        yes = self.get_argument('yes', '')
        no = self.get_argument('no', '')

        if yes:
            ids_yes = map(int, yes.split(' '))
        else:
            ids_yes = []

        if no:
            ids_no = map(int, no.split(' '))
        else:
            ids_no = []

        for i in ids_yes:
            pic_yes(i, current_user_id)

        for i in ids_no:
            pic_no(i, current_user_id)

        self.redirect(self.request.path)


@urlmap('/pic/reviewed(%s)/(0|1)' % CID_PIC)
@urlmap('/pic/reviewed(%s)/(0|1)-(\d+)' % CID_PIC)
class Reviewed(Base):
    def get(self, cid, state, n=1):
        path_base = self.request.path.split('-', 1)[0]
        total = pic_reviewed_count_by_cid_state(cid, state)
        page, limit, offset = page_limit_offset(
            '%s-%%s' % path_base,
            total,
            n,
            PAGE_LIMIT,
        )
        if type(n) == str and offset >= total:
            return self.redirect(path_base)
        pic_list = pic_list_reviewed_by_cid_state(cid, state, limit, offset)
        Zsite.mc_bind(pic_list, 'user', 'user_id')
        self.render(
            cid=int(cid),
            state=int(state),
            pic_list=pic_list,
            total=total,
            page=page,
        )
