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
from kv import Kv
from po import Po
from fs import fs_url_jpg
from zkit.fetch_pic import fetch_pic

PoPicPos = Kv('po_pic_pos')

class PoPicShow(McModel):
    pass

class PicWallPics(McModel):
    pass

def new_pic_wall_pic(url,title,description):
    new_pic = new_pic_wall_pic(url=url, title = title, description = description)
    new_pic.save()
    return new_pic

def approve_pic(id):
    pic = PicWallPics.mc_get(id)
    if pic:
        img = fetch_pic(pic.url)


def get_new_user_wall_pos(user_id):
    #TODO:改offset的取值
    c = PoPicShow.raw_sql('select * from po_pic_show order by id desc limit 1 offset 0')
    r = c.fetchone()
    if r:
        return r[0]
        
def get_current_user_wall_pic(user_id):
    pos = PoPicPos.get(user_id)
    if not pos:
        init_pos = get_new_user_wall_pos(user_id)
        PoPicPos.set(user_id,init_pos)
    return pos

def next_wall_pic(user_id):
    pos = get_current_user_wall_pic(user_id)
    wall_pic = PoPicShow.mc_get(pos)

    next_pos = pos+1
    if next_pos <= PoPicShow.max_id():
        PoPicPos.set(user_id, next_pos)

    if wall_pic:
        po = Po.mc_get(wall_pic.po_id)
        return fs_url_jpg(721,po.rid)

if __name__ == '__main__':
    #PoPicShow(po_id=65117).save()
    print next_wall_pic(10031395)
