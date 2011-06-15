#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCacheA, McCache
from tag import Tag, tag_new
from zweb.orm import ormiter

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

ZSITE_TAG = (
    6, # 转载收藏
    5, # 指点江山
    4, # 知识整理
    3, # 职业感悟
    2, # 愿景计划
    1, # 随笔杂记
)


mc_zsite_tag_id_list_by_zsite_id = McCacheA('ZsiteTagIdListByZsiteId:%s')
mc_tag_id_by_po_id = McCache('TagIdByPoId:%s')


class ZsiteTag(McModel):
    pass

class ZsiteTagPo(McModel):
    pass

@mc_zsite_tag_id_list_by_zsite_id('{zsite_id}')
def zsite_tag_id_list_by_zsite_id(zsite_id):
    return ZsiteTag.where(zsite_id=zsite_id).order_by('id desc').field_list(field='tag_id')

def zsite_tag_list_by_zsite_id(zsite_id):
    tag_id_list = zsite_tag_id_list_by_zsite_id(zsite_id)
    return Tag.value_by_id_list(tag_id_list)

def zsite_tag_new_by_zsite_id_tag_id(zsite_id, tag_id):
    zsite_tag = ZsiteTag.get_or_create(zsite_id=zsite_id, tag_id=tag_id)
    if not zsite_tag.id:
        zsite_tag.save()
        mc_zsite_tag_id_list.delete(zsite_id)
    return zsite_tag.id

def zsite_tag_list_by_zsite_id_with_init(zsite_id):
    tag_id_list = zsite_tag_id_list_by_zsite_id(zsite_id)
    if not tag_id_list:
        for tag_id in ZSITE_TAG:
            zsite_tag_new_by_zsite_id_tag_id(zsite_id, tag_id)
    tag_id_list = zsite_tag_id_list_by_zsite_id(zsite_id)
    #print tag_id_list        
    return Tag.value_by_id_list(tag_id_list)

@mc_tag_id_by_po_id('{zsite_id}_{po_id}')
def tag_id_by_po_id(zsite_id, po_id):
    c = ZsiteTagPo.raw_sql(
        'select zsite_tag_id from zsite_tag_po where zsite_id=%s and po_id=%s',
        zsite_id, po_id
    )
    r = c.fetchone()
    if r:
        r = r[0]
        tag = ZsiteTag.mc_get(r)
        r = tag.tag_id
    else:
        r = 0
    return r


def zsite_tag_new_by_tag_id(po, tag_id):
    if not Tag.get(tag_id):
        tag_id = 1
    zsite_id = po.user_id
    po_id = po.id

    id = zsite_tag_new_by_zsite_id_tag_id(zsite_id, tag_id)
    tag_po = ZsiteTagPo.get_or_create(
        po_id=po_id,
        zsite_id=zsite_id
    )
    tag_po.zsite_tag_id = id
    tag_po.save()
    mc_tag_id_by_po_id.set('%s_%s'%(zsite_id, po_id), tag_id)


def zsite_tag_new_by_tag_name(po, name):
    tag_id = tag_new(name)
    return zsite_tag_new_by_tag_id(po, tag_id)

def zsite_tag_id_mv(zsite_id, from_tag_id, to_tag_id=1):
    tag = ZsiteTag.get(zsite_id=zsite_id, tag_id=from_tag_id)

    for i in ormiter(ZsiteTagPo, 'zsite_tag_id=%s'%tag.id):
        i.zsite_tag_id = to_tag_id
        i.save()
        po_id = i.po_id
        mc_tag_id_by_po_id.set('%s_%s'%(zsite_id, po_id), to_tag_id)


def zsite_tag_rm_by_tag_id(zsite_id, tag_id):
    tag_id = int(tag_id)
    if tag_id == 1 or tag_id not in zsite_tag_id_list_by_zsite_id(zsite_id):
        return
    zsite_tag_id_mv(zsite_id, tag_id , 1)
    ZsiteTag.where(zsite_id=zsite_id,tag_id=tag_id).delete()
    mc_zsite_tag_id_list_by_zsite_id.delete(zsite_id)


if __name__ == '__main__':
    print tag_id_by_po_id(11, 12)


