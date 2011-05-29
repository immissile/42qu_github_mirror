#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel
from reply import ReplyMixin, STATE_ACTIVE, STATE_SECRET

"""
CREATE TABLE `wall` (
  `id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  `zsite_id` INTEGER UNSIGNED NOT NULL,
  `other_id` INTEGER UNSIGNED NOT NULL,
  `last_reply_id` INTEGER UNSIGNED NOT NULL,
  `reply_count` INTEGER UNSIGNED NOT NULL DEFAULT 0,
  `last_reply_zsite_id` INTEGER UNSIGNED NOT NULL,
  `create_time` INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `zsite_id`(`zsite_id`, `create_time`)
)
"""

class Wall(McModel):
    pass

