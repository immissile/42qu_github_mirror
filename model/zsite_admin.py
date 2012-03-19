#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _db import cursor_by_table, McModel, McCache, McNum, McCacheA
from zsite import Zsite
from model.cid import CID_SITE
from zkit.algorithm.wrandom import sample_or_shuffle
from model.zsite_list import zsite_list_new, STATE_ACTIVE, zsite_list_get, zsite_list_id_get, zsite_list_rm, zsite_list_count_by_zsite_id , zsite_list_id_state, ZsiteList, zsite_id_list_by_zsite_id, mc_zsite_list_id_state, STATE_ACTIVE, STATE_ADMIN, STATE_OWNER


mc_zsite_id_list_by_admin_id = McCacheA('ZsiteIdListBYAdminId.%s')
mc_admin_id_list_by_zsite_id = McCacheA('AdminIdListByZsiteId.%s')
zsite_by_admin_id_count = McNum(
    lambda id:ZsiteList.where(
        cid=CID_SITE,
        owner_id=id
    ).where('state>%s' % STATE_ADMIN).count(),
    'ZsiteByAdminIdTotal.%s'
)


def zsite_admin_new(zsite_id, admin_id, state=STATE_OWNER):
    if zsite_id and admin_id:
        cid = CID_SITE
        zsite = zsite_list_get(
            zsite_id,
            admin_id,
            cid
        )
        if not zsite:
            zsite = zsite_list_new(
                zsite_id,
                admin_id,
                cid,
                1,
                state
            )
        else:
            zsite.state = state
            zsite.save()
        mc_flush(zsite_id, admin_id)

def mc_flush(zsite_id, admin_id):
    mc_admin_id_list_by_zsite_id.delete(zsite_id)
    mc_zsite_id_list_by_admin_id.delete(admin_id)
    zsite_by_admin_id_count.delete(admin_id)
    mc_zsite_list_id_state.delete('%s_%s_%s'%(zsite_id, admin_id, CID_SITE))

@mc_admin_id_list_by_zsite_id('{id}')
def admin_id_list_by_zsite_id(id):
    return ZsiteList.where(
        cid=CID_SITE,
        zsite_id=id
    ).where('state>=%s' % STATE_ADMIN).order_by('id desc').col_list(col='owner_id')

@mc_zsite_id_list_by_admin_id('{id}')
def zsite_id_list_by_admin_id(id):
    return ZsiteList.where(
        cid=CID_SITE,
        owner_id=id
    ).where('state>=%s' % STATE_ADMIN).order_by('id desc').col_list(col='zsite_id')



def zsite_id_list_by_admin_id_sample(id, k):
    id_list = zsite_id_list_by_admin_id(id)
    if len(id_list) > k:
        id_list = sample_or_shuffle(id_list, k)
    return id_list


def zsite_list_by_admin_id(id, limit=None, offset=0):
    id_list = zsite_id_list_by_admin_id(id)

    if id_list and (offset or limit is not None):
        id_list = id_list[offset:offset+limit]
    return Zsite.mc_get_list(id_list)

def zsite_admin_rm(zsite_id, admin_id):
    cid = CID_SITE
    zsite = zsite_list_get(
        zsite_id,
        admin_id,
        cid
    )
    if zsite and zsite.state > STATE_ACTIVE:
        zsite.state = STATE_ACTIVE
        zsite.save()
        mc_flush(zsite_id, admin_id)

def zsite_admin_empty(zsite_id):
    for i in ZsiteList.where(cid=CID_SITE, zsite_id=zsite_id).where('state>%s'%STATE_ACTIVE):
        i.state = STATE_ACTIVE
        i.save()
        mc_zsite_id_list_by_admin_id.delete(admin_id)
    mc_admin_id_list_by_zsite_id.delete(zsite_id)

def zsite_user_state(zsite_id, user_id):
    if not user_id:
        return 0
    return zsite_list_id_state(zsite_id, user_id, CID_SITE)[1]



if __name__ == '__main__':
    zsite_admin_new(10126043,10018800)
    #from model.zsite import Zsite
    #class ZsiteAdmin(McModel):
    #    pass
    #for i in ZsiteAdmin.where('state>0'):

    #    zsite_id = i.zsite_id
    #    admin_id = i.admin_id

    #    site = Zsite.mc_get(zsite_id)
    #    if site.cid == CID_SITE:
    #        if zsite_id and admin_id:
    #            zsite_admin_new(zsite_id, admin_id)
    #            print zsite_id, admin_id


