#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCacheA
from tag import Tag

#CREATE TABLE  `zpage`.`zpage_tag` (
#  `id` int(10) unsigned NOT NULL auto_increment,
#  `zsite_id` int(10) unsigned NOT NULL,
#  `tag_id` int(10) unsigned NOT NULL,
#  PRIMARY KEY  (`id`),
#  KEY `tag_id` USING BTREE (`tag_id`),
#  KEY `zsite_id` (`zsite_id`,`tag_id`)
#) ENGINE=MyISAM DEFAULT CHARSET=binary;
#
#CREATE TABLE `zpage`.`zsite_tag_po` (
#  `id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
#  `zsite_tag_id` INTEGER UNSIGNED NOT NULL DEFAULT 0,
#  `po_id` INTEGER UNSIGNED NOT NULL,
#  `zsite_id` INTEGER UNSIGNED NOT NULL,
#  `state` INTEGER UNSIGNED NOT NULL,
#  PRIMARY KEY (`id`),
#  INDEX `zsite_tag_id`(`zsite_tag_id`, `po_id`,`state`),
#  INDEX `po_id` ( `po_id`,`zsite_id`)
#)ENGINE = MyISAM;

mc_zsite_tag_id_list = McCacheA("ZsiteTagIdListByZsiteId:%s")


class ZsiteTag(Model):
    pass

class ZsiteTagPo(McModel):
    pass

def zsite_tag_init(zsite_id):
    pass




@mc_zsite_tag_id_list("{zsite_id}")
def zsite_tag_id_list_by_zsite_id(zsite_id):
    return ZsiteTag.where(zsite_id=zsite_id).field_list(field='tag_id')

def zsite_tag_list_by_zsite_id(zsite_id):
    return Tag.value_by_id_list(
        zsite_tag_id_list_by_zsite_id(zsite_id)
    )    


if __name__ == "__main__":
    print zsite_tag_list_by_zsite_id(1)


