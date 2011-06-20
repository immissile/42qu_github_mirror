#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.zsite import Zsite
from model.zsite_list_0 import zsite_show_new, zsite_show_rm
from model.zsite_link import url_new
from model.user_mail import mail_by_user_id
from model.mail import sendmail

from model.cid import CID_ICO, CID_ICO96, CID_PIC
from model.pic import Pic, pic_need_review, pic_list_to_review_by_cid, pic_list_reviewed_by_cid_state
from model.ico import ico

PAGE_LIMIT = 16

@urlmap('/pic/review/ico')
class ReviewIco(Base):
    def get(self, cid):
        current_user_id = self.current_user_id
        pic_list = pic_list_to_review_by_cid(CID_ICO, PAGE_LIMIT)
        li = []
        for i in pic_list:
            if i.id == ico.get(i.user_id):
                li.append(i)
            else:
                i.state = 1
                i.save()
