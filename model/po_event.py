#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import McCache, McNum
from cid import CID_EVENT
from po import Po, po_new, po_word_new, po_note_new, po_rm, po_cid_set
from state import STATE_DEL, STATE_SECRET, STATE_ACTIVE
from txt import txt_new, txt_get
from zkit.time_format import time_title
from zsite import Zsite
from model.cid import CID_EVENT
from model.pic import pic_new_save , fs_url_jpg , fs_set_jpg
from zkit.pic import pic_fit
from event import EVENT_CID, EVENT_CID_CN



def po_event_pic_new(zsite_id, pic):
    pic_id = pic_new_save(CID_EVENT, zsite_id, pic)
    pic162 = pic_fit(pic, 162)
    fs_set_jpg(162, pic_id, pic162)
    return pic_id


def po_event_new(zsite_id, pid, address, transport, begin_time, end_time, state):
    pass



if __name__ == '__main__':
    print EVENT_CID







