#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fs import fs_set_jpg, fs_url_jpg, fs_file_jpg, fs_get_jpg
from kv import Kv
from cid import CID_ICO, CID_ICO96
from zkit.pic import pic_square, picopen, pic_zoom_inner, pic_fit_height_if_high
from pic import pic_new, pic_save
import Image

ico = Kv('ico')
ico96 = Kv('ico96')
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
#fs_file_jpg

def ico_pos_new(id, pos):
    if pos == ico_pos.get(id):
        return

    f = ico.get(id)
    if not f:
        return

    pic = picopen(fs_get_jpg('1', f))
    if not pic:
        return

    pic_id = pic_new(CID_ICO96, id)
    pos_tuple = pos.split('-')

    if len(pos_tuple) == 3:
        x, y, size = map(int, pos_tuple)
        if size:
            pic = pic_square(pic, size, top_left=(x, y), size=size)

    pic = pic_square(pic, 96, size=96)
    fs_set_jpg('96', pic_id, pic)
    ico_pos.set(id, pos)
    ico96.set(id, pic_id)

def ico_new(id, pic):
    pic_id = pic_new(CID_ICO, id)
    pic_save(pic_id, pic)
    ico_save(pic_id, pic)
    ico.set(id, pic_id)
    if not ico_pos.get(id):
        ico_pos_new(id, '')
    else:
        ico_pos.set(id, '0-0-0')
    return pic_id

def ico_save(pic_id, pic):
    p1 = pic_fit_height_if_high(pic, 721, 406)
    fs_set_jpg('1', pic_id, p1)

    p2 = p1.resize((470, 264), Image.ANTIALIAS)
    fs_set_jpg('2', pic_id, p2)

    p3 = p2.resize((219, 123), Image.ANTIALIAS)
    fs_set_jpg('3', pic_id, p3)

def pic_url(id, size='1'):
    f = ico.get(id)
    if f:
        return fs_url_jpg(size, f)

def ico_url(id):
    pic_id = ico96.get(id)
    if pic_id:
        return fs_url_jpg('96', pic_id)

if __name__ == '__main__':
    print ico_url(10024803)


