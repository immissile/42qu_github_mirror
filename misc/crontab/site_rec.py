#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from model.zsite import Zsite
from model.cid import CID_SITE, CID_NOTE, CID_USER
from zkit.single_process import single_process
from model.site_po import po_cid_count_by_zsite_id
from zweb.orm import ormiter
from model.zsite_site import zsite_id_list_by_user_id


def can_rec_site_id_list():
    result = []
    for i in ormiter(Zsite, 'cid=%s'%CID_SITE):
        zsite_id = i.id
        count = po_cid_count_by_zsite_id(zsite_id, CID_NOTE)
        if count >= 2:
            result.append(zsite_id)
    return set(result)


def user_id_site_can_rec():
    id_list = can_rec_site_id_list()

    for i in ormiter(Zsite, 'cid=%s'%CID_USER):
        user_id = i.id
        fav_site_id_set = set(zsite_id_list_by_user_id(user_id))
        can_rec_id_list = id_list - fav_site_id_set
        if not can_rec_id_list:
            continue




@single_process
def main():
    site_rec()

if __name__ == '__main__':
    main()

