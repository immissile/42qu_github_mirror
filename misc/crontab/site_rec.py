#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from model.zsite import Zsite
from model.cid import CID_SITE, CID_NOTE, CID_USER
from zkit.single_process import single_process
from model.site_po import po_cid_count_by_zsite_id
from zweb.orm import ormiter
from model.zsite_site import zsite_id_list_by_user_id
from model.site_rec import SiteRecHistory, SiteRec, site_rec_set
from random import choice
from model.top_rec import top_rec, TOP_REC_CID_OAUTH_BINDED, TOP_REC_CID_SITE_REC

def can_rec_site_id_list():
    result = []
    for i in ormiter(Zsite, 'cid=%s'%CID_SITE):
        zsite_id = i.id
        count = po_cid_count_by_zsite_id(zsite_id, CID_NOTE)
        if count > 5:
            result.append(zsite_id)
    return set(result)


def user_id_site_can_rec():
    id_list = can_rec_site_id_list()

    for i in ormiter(Zsite, 'cid=%s'%CID_USER):
        user_id = i.id
        if TOP_REC_CID_SITE_REC&top_rec(user_id) and SiteRec.get(user_id):
            continue
        fav_list = list(zsite_id_list_by_user_id(user_id))
        fav_list.extend(
            SiteRecHistory.where(user_id=user_id).col_list(col='zsite_id')
        )

        fav_site_id_set = set(fav_list)
        can_rec_id_list = id_list - fav_site_id_set

        if not can_rec_id_list:
            continue

        yield user_id, can_rec_id_list


def site_rec_by_user_id(user_id, can_rec_id_list):
    site_id = choice(list(can_rec_id_list))
    return site_id

def run():
    for user_id, can_rec_id_list in user_id_site_can_rec():
        print user_id
        site_id = site_rec_by_user_id(user_id, can_rec_id_list)
        site_rec_set(user_id, site_id)

@single_process
def main():
    run()


if __name__ == '__main__':
    main()

