#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel
from reply import ReplyMixin, STATE_ACTIVE, STATE_SECRET
from model import Zsite
from time import time
"""
CREATE TABLE `wall` (
  `id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  `cid` TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
)

CREATE TABLE `wall_reply` (
  `id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  `wall_id` INTEGER UNSIGNED NOT NULL,
  `zsite_id` INTEGER UNSIGNED NOT NULL,
  `other_id` INTEGER UNSIGNED NOT NULL,
  `reply_count` INTEGER UNSIGNED NOT NULL DEFAULT 0,
  `last_reply_id` INTEGER UNSIGNED NOT NULL 0,
  `create_time` INTEGER UNSIGNED NOT NULL,
  INDEX `zsite_id`(`zsite_id`, `last_reply_id`, `create_time`),
  UNIQUE INDEX `zw`(`zsite_id`, `wall_id`)
)
"""

class Wall(McModel, ReplyMixin):
    pass


class WallReply(McModel):
    pass


def reply_new(user_id, txt, state=STATE_ACTIVE):
    zsite_id = self.id
    reply = WallReply.get(zsite_id=zsite_id, other_id=other_id)
    now = int(time())
    if reply is None:
        wall = Wall(cid=self.cid)
        wall.save()
        reply1 = WallReply(
            wall_id=wall.id,
            zsite_id=zsite_id,
            other_id=user_id,
            create_time=now
        )
        reply1.save()
        reply2 = WallReply(
            wall_id=wall.id,
            zsite_id=user_id,
            other_id=zsite_id,
            create_time=now
        )
        reply2.save()
    else:
        pass
    wall.reply_new(current_user_id, txt, state)

Zsite.reply_new = reply_new
