#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCacheA, McLimitA
from reply import ReplyMixin, STATE_ACTIVE, STATE_SECRET
from model.zsite import Zsite
from time import time
from operator import itemgetter
from spammer import is_same_post, mc_lastest_hash

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

class Wall(McModel, ReplyMixin):
    def zsite_id_list(self):
        return (self.from_id, self.to_id)

class WallReply(McModel):
    pass

def reply_new(self, user_id, txt, state=STATE_ACTIVE):
    zsite_id = self.id
    if is_same_post(user_id, zsite_id, txt, state):
        return
    is_self = (zsite_id == user_id)
    reply1 = WallReply.get(zsite_id=zsite_id, from_id=user_id)
    if is_self:
        reply2 = reply1
    else:
        reply2 = WallReply.get(zsite_id=user_id, from_id=zsite_id)

    if reply1 is None and reply2 is None:
        wall = Wall(cid=self.cid, from_id=user_id, to_id=zsite_id)
        wall.save()
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
    mc_reply_id_list.delete(user_id)
    mc_reply_id_list.delete(zsite_id)


@mc_reply_id_list("{self.id}")
def reply_list_id_reversed(self, limit=None, offset=None):
    id_list = WallReply.where(zsite_id=self.id).where("last_reply_id>0").order_by("update_time desc").id_list(limit, offset, "last_reply_id")
    return id_list

def reply_list_reversed(self, limit=None, offset=None):
    reply_list = Wall(id=self.id, cid=self.cid)._reply_list(
        limit, offset, self.reply_list_id_reversed
    )
    return reply_list

@property
def reply_total(self):
    return Wall(id=self.id, cid=self.cid).reply_total

Zsite.reply_new = reply_new
Zsite.reply_total = reply_total
Zsite.reply_list_id_reversed = reply_list_id_reversed
Zsite.reply_list_reversed = reply_list_reversed




