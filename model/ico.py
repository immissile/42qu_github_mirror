#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fs import fs_set_jpg, fs_url_jpg
from kv import Kv
from cid import CID_ICO
from zkit.pic import pic_square, picopen, pic_zoom_inner, pic_fit_height_if_high
from pic import pic_new, pic_save

ico = Kv('ico')
ico_pos = Kv('ico_pos')

def ico_pos_new(user_id, pos):
    ico_pos.set(user_id, pos)

def ico_new(user_id, pic):
    pic_id = pic_new(CID_ICO, user_id)
    pic_save(pic_id, pic)
    ico_save(pic_id, pic)
    ico.set(user_id, pic_id)
    return pic_id

def ico_save(pic_id, pic):
    p1 = pic_fit_height_if_high(pic, 721, 406)
    fs_set_jpg('1', pic_id, p1)

    p2 = pic_fit_height_if_high(pic, 470, 264)
    fs_set_jpg('2', pic_id, p2)

    p3 = pic_fit_height_if_high(pic, 219, 123)
    fs_set_jpg('3', pic_id, p3)

def pic_url(id, size='1'):
    f = ico.get(id)
    if f:
        return fs_url_jpg(size, f)


