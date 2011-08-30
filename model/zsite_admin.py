#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import cursor_by_table, McModel, McLimitA, McCache, McNum
from state import STATE_DEL, STATE_SECRET, STATE_ACTIVE
from zsite import Zsite


class ZsiteAdmin(McModel):
    pass


def zsite_admin_new(zsite_id, admin_id, state=STATE_ACTIVE):
    o = ZsiteAdmin.get_or_create(zsite_id=zsite_id, admin_id=admin_id)
    o.state = state
    o.save()
    return o


def zsite_admin_rm(zsite_id, admin_id):
    o = ZsiteAdmin.get(zsite_id=zsite_id, admin_id=admin_id)
    if o.state >= STATE_ACTIVE:
        o.state = STATE_DEL
        o.save()


def zsite_rm_site_extra(zsite_id):
    for i in ZsiteAdmin.where(zsite_id=zsite_id).where('state>=%s', STATE_ACTIVE):
        i.state = STATE_DEL
        i.save()


def zsite_id_list_by_admin_id(admin_id):
    return ZsiteAdmin.where(admin_id=admin_id).where(state>=STATE_ACTIVE).col_list(col='zsite_id')


def zsite_list_by_admin_id(admin_id):
    id_list = zsite_id_list_by_admin_id(admin_id)
    return Zsite.mc_get_list(id_list)


def admin_id_list_by_zsite_id(zsite_id):
    return ZsiteAdmin.where(zsite_id=zsite_id).where(state>=STATE_ACTIVE).col_list(col='admin_id')


def admin_list_by_zsite_id(zsite_id):
    id_list = admin_id_list_by_zsite_id(zsite_id)
    return Zsite.mc_get_list(id_list)
