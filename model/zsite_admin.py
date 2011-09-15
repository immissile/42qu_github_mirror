#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _db import cursor_by_table, McModel, McLimitA, McCache, McNum, McCacheA
from state import STATE_DEL, STATE_SECRET, STATE_ACTIVE
from zsite import Zsite
from model.cid import CID_SITE

mc_zsite_id_list_by_admin_id = McCacheA('ZsiteIdListBYAdminId.%s')
mc_admin_id_list_by_zsite_id = McCacheA('AdminIdListByZsiteId.%s')

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

@mc_admin_id_list_by_zsite_id('{id}')
def admin_id_list_by_zsite_id(id):
    return ZsiteAdmin.where(
        zsite_id=id
    ).where('state>%s' % ZSITE_ADMIN_STATE_DEL).col_list(col='admin_id')

@mc_zsite_id_list_by_admin_id('{id}')
def zsite_id_list_by_admin_id(id):
    return ZsiteAdmin.where(
        admin_id=id
    ).where('state>%s' % ZSITE_ADMIN_STATE_DEL).col_list(col='zsite_id')


def zsite_admin_rm(zsite_id, admin_id):
    o = ZsiteAdmin.get(zsite_id=zsite_id, admin_id=admin_id)
    if o:
        o.state = ZSITE_ADMIN_STATE_DEL
        o.save()
        mc_flush(zsite_id, admin_id)


def zsite_admin_empty(zsite_id):
    for i in ZsiteAdmin.where(zsite_id=zsite_id).where("state>%s"%STATE_DEL):
        i.state = STATE_DEL
        i.save()
        mc_zsite_id_list_by_admin_id.delete(admin_id)
    mc_admin_id_list_by_zsite_id.delete(zsite_id)


