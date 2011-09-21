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

STATE_ACTIVE = 1
STATE_DEL = 0

mc_zsite_id_list = McLimitA('ZsiteIdList%s', 1024)

zsite_list_count = McNum(lambda owner_id, cid:ZsiteList.where(cid=cid, owner_id=owner_id).count(), 'ZsiteListCount%s')
zsite_list_count_by_zsite_id = McNum(lambda zsite_id, cid:ZsiteList.where(cid=cid, zsite_id=zsite_id).count(), 'ZsiteListCountByZsiteId%s')

mc_zsite_list_id_get = McCache("ZsiteListIdGet:%s")

class ZsiteList(Model):
    pass


@mc_zsite_id_list('{owner_id}_{cid}')
def zsite_id_list(owner_id, cid, limit=None, offset=None):
    qs = ZsiteList.where(owner_id=owner_id, cid=cid, state=1).order_by('rank desc')
    return qs.col_list(limit, offset, 'zsite_id')

def zsite_id_list_order_id_desc(owner_id, cid, limit=None, offset=None):
    qs = ZsiteList.where(owner_id=owner_id, cid=cid, state=1).order_by('id desc')
    return qs.col_list(limit, offset, 'zsite_id')

def zsite_list_new(zsite_id, owner_id, cid, rank=1, state=STATE_ACTIVE):
    if not owner_id or not zsite_id:
        return
    zsite = ZsiteList.get_or_create(
        zsite_id=zsite_id,
        owner_id=owner_id,
        cid=cid,
    )
    zsite.state = state
    if not zsite.rank:
        zsite.rank = rank
    zsite.save()
    mc_flush(owner_id, cid, zsite_id)


def mc_flush(owner_id, cid, zsite_id=0):
    key = '%s_%s' % (owner_id, cid)
    mc_zsite_id_list.delete(key)
    zsite_list_count.delete(key)
    if zsite_id:
        mc_zsite_list_id_get.delete(
            "%s_%s_%s"%(
                zsite_id, owner_id , cid
            )
        )
        zsite_list_count_by_zsite_id.delete(
            "%s_%s"%(
                zsite_id,  cid
            )
        )



def zsite_list_rm(zsite_id, owner_id, cid=None):
    if cid is None:
        cid_list = ZsiteList.where(zsite_id=zsite_id, owner_id=owner_id, state=1).col_list(col='cid')
        ZsiteList.raw_sql('update zsite_list set state=0 where zsite_id=%s and owner_id=%s', zsite_id, owner_id)
        for cid in cid_list:
            mc_flush(owner_id, cid, zsite_id)
    else:
        id = zsite_list_id_get(zsite_id, owner_id, cid)  
        if id:
            ZsiteList.where(id=id).delete() 
            mc_flush(owner_id, cid, zsite_id)

    

@mc_zsite_list_id_get("{zsite_id}_{owner_id}_{cid}")
def _zsite_list_id_get(zsite_id, owner_id, cid=0):
    o = ZsiteList.get(zsite_id=zsite_id, owner_id=owner_id, cid=cid, state=STATE_ACTIVE)
    if o:
        return o.id
    return 0

def zsite_list_id_get(zsite_id, owner_id, cid=0):
    if not owner_id or not zsite_id:
        return 0
    return _zsite_list_id_get(zsite_id, owner_id, cid)


def zsite_list_get(zsite_id, owner_id, cid=0):
    id = zsite_list_id_get(zsite_id, owner_id, cid=0)
    if id:
        return ZsiteList.get(id)


def zsite_list_rank(zsite_id, owner_id, rank):
    cid_list = ZsiteList.where(zsite_id=zsite_id, owner_id=owner_id, state=1).col_list(col='cid')
    ZsiteList.raw_sql('update zsite_list set rank=%s where zsite_id=%s and owner_id=%s', rank, zsite_id, owner_id)
    for cid in cid_list:
        mc_flush(owner_id, cid)


if __name__ == "__main__":
    pass
