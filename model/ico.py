#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fs import fs_set_jpg, fs_url_jpg
from kv import Kv
from cid import CID_ICO
from zkit.pic import pic_square, picopen, pic_zoom_inner
from pic import pic_new, pic_save

ico = Kv('ico')

def ico_new(user_id, pic):
    pic_id = pic_new(CID_ICO, user_id)
    pic_save(pic_id, pic)
    ico_save(pic_id, pic)
    ico.set(user_id, pic_id)
    return pic_id

def ico_save(pic_id, pic):
    p1 = pic_zoom_inner(pic, 640, 640)
    fs_set_jpg('1', pic_id, p1)

    p2 = pic_zoom_inner(pic, 320, 320)
    fs_set_jpg('2', pic_id, p1)

def ico_url(id, size='1'):
    f = ico.get(id)
    if f:
        return fs_url_jpg(size, f)
