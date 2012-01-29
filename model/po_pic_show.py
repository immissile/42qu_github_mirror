#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
CREATE TABLE `zpage`.`po_pic_show` (
  `id` int  NOT NULL AUTO_INCREMENT,
    `po_id` int  NOT NULL,
      PRIMARY KEY (`id`)
      )
ENGINE = MyISAM;

CREATE TABLE `zpage`.`po_pic_pos` (
  `id` int  NOT NULL,
    `value` int  NOT NULL,
      PRIMARY KEY (`id`)
      )
ENGINE = MyISAM;

CREATE TABLE `zpage`.`pic_wall_pics` (
  `id` int  NOT NULL,
    `url` text  NOT NULL,
      `title` varchar(128) ,
        `description` text  NOT NULL,
          PRIMARY KEY (`id`)
          )
ENGINE = MyISAM;


'''

import _env

from _db import  McModel
from po_photo import po_photo_new
from kv import Kv
from po import Po
from model.state import STATE_ACTIVE
from fs import fs_url_jpg
from zkit.fetch_pic import fetch_pic
from zkit.pic import picopen

STATE_WAIT = 0
STATE_ADDED = 1

PoPicPos = Kv('po_pic_pos')
class PoPicShow(McModel):
    pass

class PicWallPics(McModel):
    pass

def new_pic_wall_pic(url, title, description, state=STATE_WAIT):
    new_pic = PicWallPics(url=url, title=title, description=description, state=STATE_WAIT)
    new_pic.save()
    return new_pic

def append_new_wall():
    pic = PicWallPics.where(state=STATE_WAIT).order_by('id asc')[0]
    if pic:
        img = fetch_pic(pic.url)
        img = picopen(img)
        #TODO: po_photo_new(user_id, name, txt, img, state, zsite_id)
        po = po_photo_new(0, pic.title, pic.description, img, STATE_ACTIVE, 0)
        pic.state = STATE_ADDED
        pic.save()
        PoPicShow(po_id=po.id).save()
        return po

def get_new_user_wall_pos(user_id):
    #TODO:改offset的取值
    c = PoPicShow.raw_sql('select * from po_pic_show order by id asc limit 1 offset 0')
    r = c.fetchone()
    if r:
        return r[0]

def get_current_user_wall_pic(user_id):
    pos = PoPicPos.get(user_id)
    if not pos:
        pos = get_new_user_wall_pos(user_id)
        PoPicPos.set(user_id, pos)
    return pos

def next_wall_pic(user_id):
    pos = get_current_user_wall_pic(user_id)
    wall_pic = PoPicShow.mc_get(pos)

    next_pos = pos+1
    if next_pos <= PoPicShow.max_id():
        PoPicPos.set(user_id, next_pos)

    if wall_pic:
        po = Po.mc_get(wall_pic.po_id)
        return po.id,fs_url_jpg(721, po.rid)

if __name__ == '__main__':
    new_pic_wall_pic('http://p4.42qu.us/721/174/49326.jpg','title','desc')
    append_new_wall()
    #PoPicShow(po_id=65140).save()
    #print next_wall_pic(10031395)
    pass
