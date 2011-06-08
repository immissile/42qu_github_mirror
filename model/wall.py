#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCacheA, McLimitA, McCache
from reply import ReplyMixin, STATE_ACTIVE, STATE_SECRET
from model.zsite import Zsite
from time import time
from operator import itemgetter

"""
CREATE TABLE `wall` (
  `id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  `cid` TINYINT UNSIGNED NOT NULL ,
  `from_id` INTEGER UNSIGNED NOT NULL,
  `to_id` INTEGER UNSIGNED NOT NULL ,
  PRIMARY KEY (`id`),
  KEY `from_id` (`from_id`),
  KEY `to_id` (`to_id)
)

CREATE TABLE  `wall_reply` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `wall_id` int(10) unsigned NOT NULL,
  `zsite_id` int(10) unsigned NOT NULL,
  `from_id` int(10) unsigned NOT NULL,
  `last_reply_id` int(10) unsigned NOT NULL default '0',
  `update_time` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `Index_3` (`zsite_id`,`from_id`),
  KEY `zsite_id` (`zsite_id`,`last_reply_id`,`update_time`)
) ENGINE=MyISAM DEFAULT CHARSET=binary;
"""

mc_reply_id_list = McLimitA("WallReplyIdListReversed:%s", 512)
mc_reply_total = McCache("Zsite.reply_total:%s")

class Wall(McModel, ReplyMixin):
    def zsite_id_list(self):
        return (self.from_id, self.to_id)

    @property
    def link(self):
        return "/wall/txt/%s"%self.id

    def reply_rm(self, reply):
        reply.rm()
        id = self.id
        reply_cursor = self.reply_cursor
        reply_cursor.execute(
"select id from reply where rid=%s and cid=%s and state>=%s and (user_id=%s or user_id=%s) order by id desc limit 1",
            (
                id,
                self.cid,
                STATE_SECRET,
                self.from_id,
                self.to_id
            )
        )
        r = reply_cursor.fetchone()
        if r:
            last_reply_id = r[0]
        else:
            last_reply_id = 0
        for i in WallReply.where(wall_id=id):
            i.last_reply_id = last_reply_id
            i.save()
            mc_flush(i.zsite_id)



class WallReply(McModel):
    pass

def reply_new(self, user_id, txt, state=STATE_ACTIVE):
    zsite_id = self.id
    is_self = (zsite_id == user_id)
    reply1 = WallReply.get(zsite_id=zsite_id, from_id=user_id)
    if is_self:
        reply2 = reply1
    else:
        reply2 = WallReply.get(zsite_id=user_id, from_id=zsite_id)

    if reply1 is None and reply2 is None:
        wall = Wall(cid=self.cid, from_id=user_id, to_id=zsite_id)
        wall.save()
        from buzz import buzz_wall_new
        buzz_wall_new(user_id, zsite_id)
    else:
        if reply1:
            reply = reply1
        elif reply2:
            reply = reply2
        wall = Wall.mc_get(reply.wall_id)

    wall_id = wall.id
    reply_id = wall.reply_new(user_id, txt, state)
    if not reply_id:
        return

    now = int(time())

    def wall_reply_new(wall_id, aid, bid, last_reply_id, wall_reply):
        if wall_reply is None:
            wall_reply = WallReply(
                wall_id=wall_id,
                zsite_id=aid,
                from_id=bid,
                last_reply_id=reply_id
            )
        else:
            wall_reply.last_reply_id = reply_id
        wall_reply.update_time = now
        wall_reply.save()


    wall_reply_new(wall_id, zsite_id, user_id, reply_id, reply1)
    if not is_self:
        wall_reply_new(wall_id, user_id, zsite_id, reply_id, reply2)
    mc_flush(user_id)
    mc_flush(zsite_id)

def mc_flush(zsite_id):
    mc_reply_id_list.delete(zsite_id)
    mc_reply_total.delete(zsite_id)

@mc_reply_id_list("{self.id}")
def reply_list_id_reversed(self, limit=None, offset=None):
    id_list = WallReply.where(zsite_id=self.id).where("last_reply_id>0").order_by("update_time desc").field_list(limit, offset, "last_reply_id")
    return id_list

def reply_list_reversed(self, limit=None, offset=None):
    reply_list = Wall(id=self.id, cid=self.cid)._reply_list(
        limit, offset, self.reply_list_id_reversed
    )
    return reply_list

@property
@mc_reply_total('{self.id}')
def reply_total(self):
    return WallReply.where(zsite_id=self.id).count()


Zsite.reply_new = reply_new
Zsite.reply_total = reply_total
Zsite.reply_list_id_reversed = reply_list_id_reversed
Zsite.reply_list_reversed = reply_list_reversed
