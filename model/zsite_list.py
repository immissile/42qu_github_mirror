#coding:utf-8
from _db import Model, McModel, McCache

"""
CREATE TABLE `zsite_list` (
`id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
`cid` INTEGER UNSIGNED NOT NULL  DEFAULT 0,
`zsite_id` INTEGER UNSIGNED NOT NULL,
`owner_id` INTEGER UNSIGNED NOT NULL DEFAULT 0,
`rank` INTEGER UNSIGNED NOT NULL  DEFAULT 0,
PRIMARY KEY (`id`),
INDEX `cid_rank`(`owner_id`, `cid`, `rank`),
INDEX `rank`(`owner_id`, `rank`)
)
ENGINE = MyISAM;
"""

class ZsiteList(Model):
    pass

