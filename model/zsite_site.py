#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _db
from model.zsite import zsite_new, ZSITE_STATE_ACTIVE, Zsite
from model.cid import CID_SITE
from model.zsite_admin import zsite_admin_new, zsite_user_state, zsite_id_list_by_admin_id_sample, zsite_by_admin_id_count, zsite_id_list_by_admin_id
from model.zsite_show import zsite_show_new
from model.buzz import mq_buzz_site_new
from model.search_zsite import search_new
from model.zsite_list import zsite_id_list, MC_LIMIT_ZSITE_LIST, zsite_list_count,\
zsite_id_list_sample, STATE_ADMIN, STATE_ACTIVE
from zkit.algorithm.wrandom import sample_or_shuffle

ZSITE_STATE_SITE_PUBLIC = 40
ZSITE_STATE_SITE_SECRET = 20


ZSITE_STATE_SITE2CN = (
    (ZSITE_STATE_SITE_PUBLIC, '公开'),
    (ZSITE_STATE_SITE_SECRET, '私密'),
)

ZSITE_STATE_SITE2CN_DICT = dict(ZSITE_STATE_SITE2CN)

def site_new(name, admin_id, state):
    if state not in ZSITE_STATE_SITE2CN_DICT:
        state = ZSITE_STATE_SITE_PUBLIC

    site = zsite_new(name, CID_SITE, state)
    site_id = site.id
    zsite_admin_new(site_id, admin_id)

    if state > ZSITE_STATE_SITE_SECRET:
        zsite_show_new(site_id, CID_SITE)

    mq_buzz_site_new(admin_id, site_id)
    search_new(site_id)
    return site

def site_count_by_state(state):
    qs = Zsite.where(cid=CID_SITE)

    if state:
        qs = qs.where(state=state)

    return qs.count()

def site_id_list_by_state(state, limit=None, offset=None):
    qs = Zsite.where(cid=CID_SITE)

    if state:
        qs = qs.where(state=state)

    return qs.order_by('id desc').col_list(limit, offset, 'id')

def site_can_view(zsite, user_id):

    if zsite.state >= ZSITE_STATE_SITE_PUBLIC:
        return True

    zsite_id = zsite.id
    if zsite_user_state(zsite_id, user_id) >= STATE_ACTIVE:
        return True

def site_can_admin(zsite_id, user_id):
    if zsite_user_state(zsite_id, user_id) >= STATE_ADMIN:
        return True

def zsite_id_by_zsite_user_id(zsite, user_id):
    if zsite.cid == CID_SITE:
        if site_can_view(zsite, user_id):
            return zsite.id
    return 0

def zsite_site_by_user_id_sample(user_id, k):
    id_list = zsite_id_list_sample(user_id, CID_SITE, k)
    return Zsite.mc_get_list(id_list)

def zsite_site_count(zsite_id):
    return zsite_list_count(zsite_id, CID_SITE)

def zsite_id_list_by_user_id(user_id):
    return zsite_id_list(user_id, CID_SITE)

def zsite_site_rm(zsite_id):
    from model.zsite_fav import zsite_fav_rm_all_by_ziste_id
    from model.zsite_admin import  zsite_admin_empty
    zsite_show_rm(Zsite.mc_get(zsite_id))
    zsite_fav_rm_all_by_zsite_id(zsite_id)
    zsite_admin_empty(zsite_id)

if __name__ == '__main__':
    print zsite_site_by_user_id_sample(10000000, 3)


