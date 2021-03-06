#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McLimitA, McNum, McCacheA
from model.zsite import Zsite
from zkit.algorithm.wrandom import sample_or_shuffle

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

STATE_OWNER = 60
STATE_ADMIN = 40
STATE_ACTIVE = 20
STATE_INVITE = 10
STATE_RM = 0

STATE_LIST = ( STATE_OWNER , STATE_ADMIN  , STATE_ACTIVE , STATE_INVITE , STATE_RM )


STATE_EGT_ACTIVE = 'state>=%s'%STATE_ACTIVE

MC_LIMIT_ZSITE_LIST = 1024

mc_zsite_id_list = McLimitA('ZsiteIdList%s', MC_LIMIT_ZSITE_LIST)
mc_zsite_id_list_by_zsite_id = McLimitA('ZsiteIdListByZsiteId%s', MC_LIMIT_ZSITE_LIST)
mc_zsite_id_list_active = McLimitA('ZsiteIdListActive%s', MC_LIMIT_ZSITE_LIST)
mc_zsite_id_list_by_zsite_id_state = McLimitA('ZsiteIdListByZsiteIdActive%s', MC_LIMIT_ZSITE_LIST)

zsite_list_count_active = McNum(lambda owner_id, cid:ZsiteList.where(cid=cid, owner_id=owner_id, state=STATE_ACTIVE).count(), 'ZsiteListCount%s')
zsite_list_count = McNum(lambda owner_id, cid:ZsiteList.where(cid=cid, owner_id=owner_id).where(STATE_EGT_ACTIVE).count(), 'ZsiteListCount%s')
zsite_list_count_by_zsite_id = McNum(lambda zsite_id, cid:ZsiteList.where(cid=cid, zsite_id=zsite_id).where('owner_id>0').where(STATE_EGT_ACTIVE).count(), 'ZsiteListCountByZsiteId%s')

mc_zsite_list_id_state = McCacheA('ZsiteListIdState:%s')

class ZsiteList(McModel):
    pass

def zsite_list_active(owner_id, cid, limit=None, offset=None):
    return Zsite.mc_get_list(
        zsite_id_list_active(owner_id, cid, limit, offset)
    )


def zsite_list(owner_id, cid, limit=None, offset=None):
    return Zsite.mc_get_list(
        zsite_id_list(owner_id, cid, limit, offset)
    )

@mc_zsite_id_list('{owner_id}_{cid}')
def zsite_id_list(owner_id, cid, limit=None, offset=None):
    qs = ZsiteList.where(owner_id=owner_id, cid=cid).where(STATE_EGT_ACTIVE).order_by('rank desc')
    return qs.col_list(limit, offset, 'zsite_id')

@mc_zsite_id_list_by_zsite_id('{zsite_id}_{cid}')
def zsite_id_list_by_zsite_id(zsite_id, cid, limit=None, offset=None):
    qs = ZsiteList.where(zsite_id=zsite_id, cid=cid).where(STATE_EGT_ACTIVE).where('owner_id>0').order_by('rank desc, id desc')
    return qs.col_list(limit, offset, 'owner_id')


@mc_zsite_id_list_active('{owner_id}_{cid}')
def zsite_id_list_active(owner_id, cid, limit=None, offset=None):
    qs = ZsiteList.where(owner_id=owner_id, cid=cid, state=STATE_ACTIVE).order_by('rank desc')
    return qs.col_list(limit, offset, 'zsite_id')

def zsite_id_list_by_zsite_id_active(zsite_id, cid, limit=None, offset=None):
    return zsite_id_list_by_zsite_id_state(zsite_id, cid, STATE_ACTIVE, limit, offset)

@mc_zsite_id_list_by_zsite_id_state('{zsite_id}_{cid}_{state}')
def zsite_id_list_by_zsite_id_state(zsite_id, cid, state, limit=None, offset=None):
    qs = ZsiteList.where(zsite_id=zsite_id, cid=cid, state=state).where('owner_id>0').order_by('rank desc')
    return qs.col_list(limit, offset, 'owner_id')


def zsite_list_by_zsite_id_state(zsite_id, cid, state, limit=None, offset=None):
    return Zsite.mc_get_list(
        zsite_id_list_by_zsite_id_state(zsite_id, cid, state, limit, offset)
    )

def zsite_id_list_order_id_desc(owner_id, cid, limit=None, offset=None):
    qs = ZsiteList.where(owner_id=owner_id, cid=cid).where(STATE_EGT_ACTIVE).order_by('id desc')
    return qs.col_list(limit, offset, 'zsite_id')

def zsite_list_new(zsite_id, owner_id, cid, rank=1, state=STATE_ACTIVE):
    if zsite_id is None:
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
    mc_flush(owner_id, cid, zsite_id, state)
    return zsite


def mc_flush(owner_id, cid, zsite_id=0, state=None):
    key = '%s_%s' % (owner_id, cid)
    mc_zsite_id_list.delete(key)
    zsite_list_count.delete(key)
    mc_zsite_id_list_active.delete(key)
    zsite_list_count_active.delete(key)

    if zsite_id:
        mc_zsite_id_list_by_zsite_id.delete('%s_%s'%(zsite_id, cid))
        for state in STATE_LIST:
            mc_zsite_id_list_by_zsite_id_state.delete('%s_%s_%s'%(zsite_id, cid, state))

        mc_zsite_list_id_state.delete(
            '%s_%s_%s'%(
                zsite_id, owner_id , cid
            )
        )
        zsite_list_count_by_zsite_id.delete(
            '%s_%s'%(
                zsite_id, cid
            )
        )


def zsite_list_rm(zsite_id, owner_id, cid=None):
    if cid is None:
        cid_list = ZsiteList.where(zsite_id=zsite_id, owner_id=owner_id, state=1).col_list(col='cid')
        ZsiteList.raw_sql('update zsite_list set state=0 where zsite_id=%s and owner_id=%s', zsite_id, owner_id)
        for cid in cid_list:
            mc_flush(owner_id, cid, zsite_id)
    else:
        id, state = zsite_list_id_state(zsite_id, owner_id, cid)
        if id:
            ZsiteList.where(id=id).delete()
            mc_flush(owner_id, cid, zsite_id)


@mc_zsite_list_id_state('{zsite_id}_{owner_id}_{cid}')
def zsite_list_id_state(zsite_id, owner_id, cid):
    o = ZsiteList.get(zsite_id=zsite_id, owner_id=owner_id, cid=cid)
    if o:
        return o.id, o.state
    return 0 , 0

def _zsite_list_id_get(zsite_id, owner_id, cid=0):
    id, state = zsite_list_id_state(zsite_id, owner_id, cid)
    if state >= STATE_ACTIVE:
        return id
    return 0

def zsite_list_id_get(zsite_id, owner_id, cid=0):
    if not zsite_id:
        return 0
    return _zsite_list_id_get(zsite_id, owner_id, cid)


def zsite_list_get(zsite_id, owner_id, cid=0):
    id = zsite_list_id_get(zsite_id, owner_id, cid=cid)
    if id:
        return ZsiteList.mc_get(id)


def zsite_list_rank(zsite_id, owner_id, rank):
    cid_list = ZsiteList.where(zsite_id=zsite_id, owner_id=owner_id, state=1).col_list(col='cid')
    ZsiteList.raw_sql('update zsite_list set rank=%s where zsite_id=%s and owner_id=%s', rank, zsite_id, owner_id)
    for cid in cid_list:
        mc_flush(owner_id, cid)


def zsite_id_list_sample(zsite_id, cid, k):
    a = zsite_id_list(zsite_id, cid, MC_LIMIT_ZSITE_LIST, 0)
    a = sample_or_shuffle(a, k)
    return a


def zsite_list_sample(zsite_id, cid, k):
    return Zsite.mc_get_list(
        zsite_id_list_sample(zsite_id, cid, k)
    )

if __name__ == '__main__':
    #$pass
    #$from model.cid import CID_PRODUCT
    #$for i in ZsiteList.where(cid=CID_PRODUCT):
    #$    i.delete()

    print zsite_list_id_get(64278,51168,cid=6)
