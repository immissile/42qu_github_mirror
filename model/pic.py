#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache
from kv_table import KvTable
from zkit.pic import pic_square, picopen, pic_zoom_inner
from time import time
from fs import fs_set_jpg, fs_url_jpg
from tid import TID_ICO

ico = KvTable('ico')

class Pic(Model):
    pass

def pic_new(tid, zsite_id):
    p = Pic(
        tid=tid,
        zsite_id=zsite_id,
        create_time=int(time()),
    ).save()
    return p.id

def pic_save(pic_id, pic):
    fs_set_jpg('0', pic_id, pic)

def ico_new(zsite_id, pic):
    pic_id = pic_new(TID_ICO, zsite_id)
    pic_save(pic_id, pic)
    ico_save(pic_id, pic)
    ico.set(zsite_id, pic_id)
    return pic_id

def ico_save(pic_id, pic):
    p1 = pic_zoom_inner(pic, 640, 640)
    fs_set_jpg('1', pic_id, p1)

    p2 = pic_zoom_inner(pic, 320, 320)
    fs_set_jpg('2', pic_id, p1)

def ico_url(id, size='1'):
    f = ico.get(id)
    if f:
        url = fs_url_jpg(size, f)
        return url
