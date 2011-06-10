#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McLimitA

'''
CREATE TABLE `zsite_list` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `zsite_id` int(10) unsigned NOT NULL,
  `owner_id` int(10) unsigned NOT NULL,
  `cid` int(10) unsigned NOT NULL,
  `state` tinyint(3) unsigned NOT NULL,
  `rank` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `zsite` (`zsite_id`,`owner_id`,`cid`),
  KEY `cid_rank` (`owner_id`,`cid`,`state`,`rank`)
) ENGINE=MyISAM;
'''

class ZsiteList(Model):
    pass

STATE_ACTIVE = 1
STATE_DEL = 0

mc_zsite_list = McLimitA('ZsiteList%s', 1024)

@mc_zsite_list('{owner_id}_{cid}')
def zsite_list(owner_id, cid, limit=None, offset=None):
    qs = ZsiteList.where(owner_id=owner_id, cid=cid, state=1).order_by('rank desc')
    return qs.field_list(limit, offset, 'zsite_id')

def _zsite_list_new(zsite_id, owner_id, cid, rank=1000):
    zsite = ZsiteList.get_or_create(
        zsite_id=zsite_id,
        owner_id=owner_id,
        cid=cid,
    )
    zsite.state = 1
    zsite.rank = rank
    zsite.save()
    mc_zsite_list.delete('%s_%s' % (owner_id, cid))

def zsite_list_new(zsite_id, owner_id, cid_list=[], rank=1000):
    cid_list = set(cid_list)
    cid_list.add(0)
    for cid in cid_list:
        _zsite_list_new(zsite_id, owner_id, cid, rank)

def zsite_list_rm(zsite_id, owner_id):
    cid_list = ZsiteList.where(zsite_id=zsite_id, owner_id=owner_id, state=1).field_list(field='cid')
    ZsiteList.raw_sql('update zsite_list state=0 where zsite_id=%s and owner_id=%s', zsite_id, owner_id)
    for cid in cid_list:
        mc_zsite_list_id_0.delete('%s_%s' % (owner_id, cid))

def zsite_list_get(zsite_id, owner_id, cid=0):
    return ZsiteList.get(zsite_id=zsite_id, owner_id=owner_id, cid=cid, state=1)

def zsite_list_rank(zsite_id, owner_id, rank):
    cid_list = ZsiteList.where(zsite_id=zsite_id, owner_id=owner_id, state=1).field_list(field='cid')
    ZsiteList.raw_sql('update zsite_list rank=%s where zsite_id=%s and owner_id=%s', rank, zsite_id, owner_id)
    for cid in cid_list:
        mc_zsite_list_id_0.delete('%s_%s' % (owner_id, cid))
