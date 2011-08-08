#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _db import McModel
from operator import itemgetter
from model.gid import gid

"""
CREATE TABLE  `zpage`.`event` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `city_pid` int(10) unsigned NOT NULL,
  `pid` int(10) unsigned NOT NULL,
  `address` varchar(255) collate utf8_bin NOT NULL,
  `transport` varchar(255) collate utf8_bin NOT NULL,
  `begin_time` int(10) unsigned NOT NULL default '0',
  `end_time` int(10) unsigned NOT NULL default '0',
  `cent` int(10) unsigned NOT NULL default '0',
  `state` tinyint(3) unsigned NOT NULL,
  `need_review` int(10) unsigned NOT NULL,
  `cid` tinyint(3) unsigned NOT NULL,
  `zsite_id` int(10) unsigned NOT NULL,
  `limit_up` int(10) unsigned NOT NULL default '0',
  `phone` varbinary(64) NOT NULL,
  `limit_down` int(10) unsigned NOT NULL,
  `pic_id` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `Index_3` (`zsite_id`),
  KEY `Index_2` USING BTREE (`state`,`limit_up`),
  KEY `Index_4` (`city_pid`,`state`)
) ENGINE=MyISAM AUTO_INCREMENT=21 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
"""

def event_new(
    zsite_id,
    cid,
    city_pid,
    pid,
    address,
    transport,
    begin_time,
    end_time,
    cent,
    need_review,
    limit_up,
    limit_down,
    phone,
    pic_id,
    id=None
):
    if id:
        event = Event.mc_get(id)
        if event.zsite_id == zsite_id:
            event.cid=cid
            event.city_pid=city_pid
            event.pid=pid
            event.address=address
            event.transport=transport
            event.begin_time=begin_time
            event.end_time=end_time
            event.cent=cent
            event.need_review=need_review
            event.limit_up=limit_up
            event.limit_down=limit_down
            event.phone=phone
            event.pic_id=pic_id
            #event.state=EVENT_STATE_INIT
            event.save()
    else:
        event = Event(
            id=gid(),
            zsite_id=zsite_id,
            cid=cid,
            city_pid=city_pid,
            pid=pid,
            address=address,
            transport=transport,
            begin_time=begin_time,
            end_time=end_time,
            cent=cent,
            need_review=need_review,
            limit_up=limit_up,
            limit_down=limit_down,
            phone=phone,
            pic_id=pic_id,
            state=EVENT_STATE_INIT
        )
        event.save()
        
    return event

class Event(McModel):
    def can_admin(self, user_id):
        if self.zsite_id == user_id:
            return True



EVENT_CID_CN = (
    (1 , '技术'),
    (2 , '创业'),
    (3 , '展览'),
    (4 , '电影'),
    (5 , '体育'),
    (6 , '旅行'),
    (7 , '公益'),
    (8 , '讲座'),
    (9 , '曲艺'),
    (10, '聚会'),
    (11, '演出'),
    (12, '其他'),
)
EVENT_CID = tuple(map(itemgetter(0), EVENT_CID_CN))
EVENT_STATE_INIT = 1
EVENT_STATE_TO_REVIEW = 5
EVENT_STATE_BEGIN = 10
EVENT_STATE_END = 15
EVENT_STATE_DEL = 20














