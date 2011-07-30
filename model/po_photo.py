#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from _db import Model, McModel, McCache, McCacheA, McLimitA, McNum, McCacheM
from cgi import escape
from zkit.pic import pic_fit_width_cut_height_if_large
from pic import pic_new, pic_save, PicMixin
from cid import CID_PHOTO
from fs import fs_set_jpg, fs_url_jpg
from model.po import po_new , txt_new , is_same_post , STATE_SECRET, STATE_ACTIVE, time_title
from po_pic import PoPic
from zsite_tag import  zsite_tag_new_by_tag_id



PIC_SIZE = 721

def photo_new(user_id, photo):
    photo_id = pic_new(CID_PHOTO, user_id)
    pic_save(photo_id, photo)
    po_photo_save(photo_id, photo)
    return photo_id

def po_photo_save(photo_id, photo):
    p1 = pic_fit_width_cut_height_if_large(photo, 721)
    fs_set_jpg('721', photo_id, p1)
    p1 = pic_fit_width_cut_height_if_large(photo, 677)
    fs_set_jpg('677', photo_id, p1)


def po_photo_new(user_id, name, txt, img, state=STATE_ACTIVE):
    if not name and not txt:
        return

    name = name or time_title()
    if not is_same_post(user_id, name, txt):

        rid = photo_new(user_id, img)

        m = po_new(CID_PHOTO, user_id, name, state, rid)
        id = m.id
        m.txt_set(txt)
        if state > STATE_SECRET:
            m.feed_new()

        zsite_tag_new_by_tag_id(m, 1)

        return m


if __name__ == '__main__':
    pass
