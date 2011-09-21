#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _db
from model.zsite import zsite_new, ZSITE_STATE_ACTIVE
from model.cid import CID_SITE
from model.zsite_admin import zsite_admin_new, zsite_user_state
from model.zsite_show import zsite_show_new

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

    return site


def site_can_view(zsite, current_user_id):

    if zsite.state >= ZSITE_STATE_SITE_PUBLIC:
        return True

    if zsite_user_state(zsite_id, user_id):
        return True

def site_can_admin(zsite_id, user_id):
    if zsite_user_state(zsite_id, user_id):
        return True



if __name__ == '__main__':
    print '..'

