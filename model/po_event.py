#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import McCache, McNum
from cid import CID_EVENT
from po import Po, po_new, po_word_new, po_note_new, po_rm, po_cid_set
from state import STATE_DEL, STATE_SECRET, STATE_ACTIVE
from txt import txt_new, txt_get
from zkit.time_format import time_title
from zsite import Zsite
from operator import itemgetter
from model.cid import CID_EVENT
from model.pic import pic_new_save , fs_url_jpg , fs_set_jpg
from zkit.pic import pic_fit

EVENT_CID_CN = (
    (1 ,"技术"),
    (2 ,"创业"),
    (3 ,"展览"),
    (4 ,"电影"),
    (5 ,"体育"),
    (6 ,"旅行"),
    (7 ,"公益"),
    (8 ,"讲座"),
    (9 ,"曲艺"),
    (10,"聚会"),
    (11,"演出"),
    (12,"其他"),
)
EVENT_CID = tuple(map(itemgetter(0),EVENT_CID_CN))



def po_event_pic_new(user_id, pic):
    pic_id = pic_new_save(CID_EVENT, user_id, pic)
    pic162 = pic_fit(pic, 162)
    fs_set_jpg(162, pic_id,pic162) 
    return pic_id


def po_event_new(user_id, name, txt, state):
    pass



if __name__ == "__main__":
    print EVENT_CID







