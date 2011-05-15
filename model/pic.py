#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache
from kv_table import KvTable
from zkit.pic import pic_fit, pic_square, picopen, pic_fit_height_if_high
"""
CREATE TABLE `pic_ico_history` (
`id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
`zpage_id` INTEGER UNSIGNED NOT NULL,
`create_time` TIMESTAMP NOT NULL,
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

pic_ico = KvTable('pic_ico')

def pic_show_save(man_id, im):
    pic_id = pic_add(man_id)
    pic_f = "%s.jpg"%pic_id
    prefix = PIC_SHOW_PREFIX

    fs_set_jpg("ico0", pic_f, im)

    pic = pic_fit_height_if_high(im, 721, 406)
    fs_set_jpg("ico1", pic_f, pic)

    pic = pic_fit_height_if_high(im, 470, 264)
    fs_set_jpg("ico2", pic_f, pic)

    pic = pic_fit_height_if_high(im, 219, 123)
    fs_set_jpg("ico3", pic_f, pic)

    pic_show_set_jpg_square(pic_id, im)
    return pic_id

def pic_new(form, error, man_id, pic_show_id):
    img = form.img
    if 'img' in form and img is not None and img.filename:
        img = picopen(img.file)
        if img:
            pos = ""
            if pic_show_id:
                pic_show_replace(img, pic_show_id)
            else:
                pic_show_id = pic_show_add(man_id, img)
            pic_show_admin_new(man_id)
            return pic_show_id
        else:
            error.img = "图片格式有误"
            return False

def pic_ico_new(id, file):
    pass

def pic_ico_url(id):
    pic_ico.get(id)


