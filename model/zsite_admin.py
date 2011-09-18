#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _db import cursor_by_table, McModel, McLimitA, McCache, McNum, McCacheA
from state import STATE_DEL, STATE_SECRET, STATE_ACTIVE
from zsite import Zsite
from model.cid import CID_SITE

mc_zsite_id_list_by_admin_id = McCacheA('ZsiteIdListBYAdminId.%s')
mc_admin_id_list_by_zsite_id = McCacheA('AdminIdListByZsiteId.%s')
mc_zsite_user_state = McCache("ZsiteUserState:%s")
zsite_by_admin_id_count = McNum(
    lambda id:ZsiteAdmin.where(
        admin_id=id
    ).where('state>%s' % ZSITE_ADMIN_STATE_DEL).count(),
    'ZsiteByAdminIdTotal.%s'
)


ZSITE_ADMIN_STATE_DEL = 0
ZSITE_ADMIN_STATE_OWNER = 100


class ZsiteAdmin(McModel):
    pass

def zsite_admin_new(zsite_id, admin_id, state=ZSITE_ADMIN_STATE_OWNER):
    zsite_admin = ZsiteAdmin.get_or_create(
        zsite_id=zsite_id,
        admin_id=admin_id,
    )
    zsite_admin.state = state
    zsite_admin.save()

    mc_flush(zsite_id, admin_id)

def mc_flush(zsite_id, admin_id):
    mc_admin_id_list_by_zsite_id.delete(zsite_id)
    mc_zsite_id_list_by_admin_id.delete(admin_id)
    zsite_by_admin_id_count.delete(admin_id)
    mc_zsite_user_state.delete("%s_%s"%(zsite_id, admin_id))

@mc_admin_id_list_by_zsite_id('{id}')
def admin_id_list_by_zsite_id(id):
    return ZsiteAdmin.where(
        zsite_id=id
    ).where('state>%s' % ZSITE_ADMIN_STATE_DEL).order_by("id desc").col_list(col='admin_id')

@mc_zsite_id_list_by_admin_id('{id}')
def zsite_id_list_by_admin_id(id):
    return ZsiteAdmin.where(
        admin_id=id
    ).where('state>%s' % ZSITE_ADMIN_STATE_DEL).order_by("id desc").col_list(col='zsite_id')


def zsite_list_by_admin_id(id, limit=None, offset=0):
    id_list = zsite_id_list_by_admin_id(id)

    if id_list and (offset or limit is not None):
        id_list = id_list[offset:offset+limit]
    return Zsite.mc_get_list(id_list)

def zsite_admin_rm(zsite_id, admin_id):
    o = ZsiteAdmin.get(zsite_id=zsite_id, admin_id=admin_id)
    if o:
        o.state = ZSITE_ADMIN_STATE_DEL
        o.save()
        mc_flush(zsite_id, admin_id)


def zsite_admin_empty(zsite_id):
    for i in ZsiteAdmin.where(zsite_id=zsite_id).where('state>%s'%STATE_DEL):
        i.state = STATE_DEL
        i.save()
        mc_zsite_id_list_by_admin_id.delete(admin_id)
    mc_admin_id_list_by_zsite_id.delete(zsite_id)

@mc_zsite_user_state("{zsite_id}_{user_id}")
def zsite_user_state(zsite_id, user_id):
    z = ZsiteAdmin.get(zsite_id=zsite_id, user_id=user_id)
    if z:
        return z.state
    return 0

if __name__ == '__main__':
    print zsite_id_list_by_admin_id(10000000)
    print zsite_list_by_admin_id(10000000)
    print zsite_by_admin_id_count(10000000)

