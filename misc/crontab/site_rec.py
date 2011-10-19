#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from model.zsite import Zsite
from model.cid import CID_SITE, CID_NOTE
from zkit.single_process import single_process
from model.site_po import po_cid_count_by_zsite_id

def can_rec_site_id_list():
    result = []
    for i in Zsite.where(cid=CID_SITE):
        zsite_id = i.id
        count = po_cid_count_by_zsite_id(zsite_id, CID_NOTE)
        if count >= 2:
            result.append(zsite_id)
    return result

def site_rec():
    id_list = can_rec_site_id_list()
    print id_list

@single_process
def main():
    site_rec()

if __name__ == '__main__':
    main()

