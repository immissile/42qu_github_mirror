#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCacheA, McLimitA, McCache
from reply import Reply, ReplyMixin, STATE_ACTIVE, STATE_SECRET
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

mc_reply_id_list = McLimitA('WallReplyIdListReversed:%s', 512)
mc_reply_total = McCache('Zsite.reply_total:%s')

class Wall(McModel, ReplyMixin):
    def zsite_id_list(self):
        return set([self.from_id, self.to_id])

    def reply_user_id_list(self):
        reply_id_list = self.reply_id_list_reversed(10)
        user_id_list = [i.user_id for i in Reply.mc_get_list(reply_id_list)]
        return set(user_id_list) - self.zsite_id_list()

    @property
    def link(self):
        return '/wall/%s' % self.id

    def reply_new(self, user_id, txt, state):
        from cid import CID_NOTICE_WALL, CID_NOTICE_WALL_REPLY
        from notice import notice_new
        reply_id = super(Wall, self).reply_new(user_id, txt, state)
        if reply_id:
            zsite_id_list = self.zsite_id_list()
            if user_id in zsite_id_list:
                zsite_id_list.remove(user_id)
                for zsite_id in zsite_id_list:
                    notice_new(user_id, zsite_id, CID_NOTICE_WALL, self.id)
            else:
                for zsite_id in zsite_id_list:
                    notice_new(user_id, zsite_id, CID_NOTICE_WALL_REPLY, self.id)
            return reply_id

    def reply_rm(self, reply):
        reply.rm()
        id = self.id
        reply_cursor = self.reply_cursor
        reply_cursor.execute(
'select id from reply where rid=%s and cid=%s and state>=%s and (user_id=%s or user_id=%s) order by id desc limit 1',
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
    @property
    def link(self):
        if not hasattr(self, '_link'):
            zsite = Zsite.mc_get(self.zsite_id)
            wall = Wall.mc_get(self.wall_id)
            self._link = '%s%s' % (zsite.link, wall.link)
        return self._link


def reply_new(self, user_id, txt, state=STATE_ACTIVE):
    zsite_id = self.id
    not_self = zsite_id != user_id
    wall_reply = reply1 = WallReply.get(zsite_id=zsite_id, from_id=user_id)
    if not_self:
        reply2 = WallReply.get(zsite_id=user_id, from_id=zsite_id)
        wall_reply = reply1 or reply2

    if wall_reply is None:
        wall = Wall(cid=self.cid, from_id=user_id, to_id=zsite_id)
        wall.save()
    else:
        wall = Wall.mc_get(wall_reply.wall_id)

    reply_id = wall.reply_new(user_id, txt, state)
    if not reply_id:
        return

    wall_id = wall.id

    if not_self:
        from buzz import mq_buzz_wall_new
        if wall_reply is None:
            if state == STATE_ACTIVE:
                mq_buzz_wall_new(user_id, zsite_id, wall_id)

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
    if not_self:
        wall_reply_new(wall_id, user_id, zsite_id, reply_id, reply2)
    mc_flush(user_id)
    mc_flush(zsite_id)


def mc_flush(zsite_id):
    mc_reply_id_list.delete(zsite_id)
    mc_reply_total.delete(zsite_id)


@mc_reply_id_list('{self.id}')
def reply_list_id_reversed(self, limit=None, offset=None):
    id_list = WallReply.where(zsite_id=self.id).where('last_reply_id>0').order_by('update_time desc').field_list(limit, offset, 'last_reply_id')
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
