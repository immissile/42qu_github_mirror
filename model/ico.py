#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fs import fs_set_jpg, fs_url_jpg
from kv import Kv
from cid import CID_ICO
from zkit.pic import pic_square, picopen, pic_zoom_inner, pic_fit_height_if_high
from pic import pic_new, pic_save

ico = Kv('ico')
ico_pos = Kv('ico_pos')
    
#show = PicShow.mc_get(id)
#if x is not None and y is not None and size and show:
#    pic_id = show.pic_id
#    img = picopen(fs_get(PIC_SHOW_PREFIX+"721", "%s.jpg"%pic_id))
#    if img is None:
#        return
#    img = pic_square(img, size, top_left=(x, y), size=size)
#    ver = show.ver + 1
#    pic_show_set_jpg_square(pic_id, img, ver)
#    show.ver = ver
#    show.save()
#
#    p = PicShowPos.get_or_create(id=id)
#    p.txt = "%s_%s_%s"%(x, y, size)
#    p.save()
#
#    mc_flush(show.man_id)

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


