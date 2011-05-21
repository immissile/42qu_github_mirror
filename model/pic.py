#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache
from kv_table import KvTable
from zkit.pic import pic_square, picopen, pic_zoom_inner
from time import time
from fs import fs_set_jpg, fs_url_jpg
"""
CREATE TABLE `pic_ico_history` (
`id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
`zsite_id` INTEGER UNSIGNED NOT NULL,
`create_time` INTEGER UNSIGNED NULL,
`admin_id` INTEGER UNSIGNED NOT NULL DEFAULT 0,
`state` TINYINT UNSIGNED NOT NULL DEFAULT 1,
INDEX `AdminId`(`admin_id`),
INDEX `State`(`state`),
PRIMARY KEY (`id`)
)ENGINE = MyISAM;

CREATE TABLE `pic_ico` (
`id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
`value` INTEGER UNSIGNED NOT NULL,
PRIMARY KEY (`id`)
)
ENGINE = MyISAM;
"""

ico = KvTable('ico')

class Pic(Model):
    pass

def pic_new(zsite_id, pic):
    p = Pic(
        zsite_id=zsite_id,
        create_time=int(time()),
    ).save()
    pic_id = p.id
    fs_set_jpg("0", pic_id, pic)

    p1 = pic_zoom_inner(pic, 640, 640)
    fs_set_jpg("1", pic_id, p1)

    p2 = pic_zoom_inner(pic, 320, 320)
    fs_set_jpg("2", pic_id, p1)
    return pic_id

def ico_new(zsite_id, pic):
    pic_id = pic_new(zsite_id, pic)
    ico.set(zsite_id, pic_id)
    return pic_id

def ico_url(id, size="1"):
    f = ico.get(id)
    if f:
        url = fs_url_jpg(size, f)
        return url
