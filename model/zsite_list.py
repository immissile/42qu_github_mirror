#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McLimitA, McNum

'''
CREATE TABLE `zsite_list` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `zsite_id` int(10) unsigned NOT NULL,
  `owner_id` int(10) unsigned NOT NULL,
  `cid` int(10) unsigned NOT NULL,
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

mc_zsite_id_list = McLimitA('ZsiteIdList%s', 1024)
zsite_list_count = McNum(lambda owner_id, cid:ZsiteList.where(cid=cid, owner_id=owner_id).count(), 'ZsiteListCount%s')


@mc_zsite_id_list('{owner_id}_{cid}')
def zsite_id_list(owner_id, cid, limit=None, offset=None):
    qs = ZsiteList.where(owner_id=owner_id, cid=cid, state=1).order_by('rank desc')
    return qs.col_list(limit, offset, 'zsite_id')

def zsite_id_list_order_id_desc(owner_id, cid, limit=None, offset=None):
    qs = ZsiteList.where(owner_id=owner_id, cid=cid, state=1).order_by('id desc')
    return qs.col_list(limit, offset, 'zsite_id')

def zsite_list_new(zsite_id, owner_id, cid, rank=1, state=STATE_ACTIVE):
    zsite = ZsiteList.get_or_create(
        zsite_id=zsite_id,
        owner_id=owner_id,
        cid=cid,
    )
    zsite.state = state
    zsite.rank = rank
    zsite.save()
    mc_flush_owner_id_cid(owner_id, cid)


def mc_flush_owner_id_cid(owner_id, cid):
    key = '%s_%s' % (owner_id, cid)
    mc_zsite_id_list.delete(key)
    zsite_list_count.delete(key)




def zsite_list_rm(zsite_id, owner_id):
    cid_list = ZsiteList.where(zsite_id=zsite_id, owner_id=owner_id, state=1).col_list(col='cid')
    ZsiteList.raw_sql('update zsite_list set state=0 where zsite_id=%s and owner_id=%s', zsite_id, owner_id)
    for cid in cid_list:
        mc_flush_owner_id_cid(owner_id, cid)


def zsite_list_get(zsite_id, owner_id, cid=0):
    return ZsiteList.get(zsite_id=zsite_id, owner_id=owner_id, cid=cid, state=1)


def zsite_list_rank(zsite_id, owner_id, rank):
    cid_list = ZsiteList.where(zsite_id=zsite_id, owner_id=owner_id, state=1).col_list(col='cid')
    ZsiteList.raw_sql('update zsite_list set rank=%s where zsite_id=%s and owner_id=%s', rank, zsite_id, owner_id)
    for cid in cid_list:
        mc_flush_owner_id_cid(owner_id, cid)

if __name__ == "__main__":
    pass
