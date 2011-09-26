#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _db
from model.zsite import zsite_new, ZSITE_STATE_ACTIVE, Zsite
from model.cid import CID_SITE
from model.zsite_admin import zsite_admin_new, zsite_user_state
from model.zsite_show import zsite_show_new
from model.buzz import mq_buzz_site_new

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
    if zsite_user_state(zsite_id, user_id):
        return True

def site_can_admin(zsite_id, user_id):
    if zsite_user_state(zsite_id, user_id):
        return True

def zsite_id_by_zsite_user_id(zsite, user_id):
    if zsite.cid == CID_SITE:
        if site_can_view(zsite, user_id):
            return zsite.id
    return 0

if __name__ == '__main__':
    print site_count_by_state(ZSITE_STATE_SITE_PUBLIC)
    print len(site_id_list_by_state(ZSITE_STATE_SITE_PUBLIC,20,20))
