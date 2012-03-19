#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import _env
import csv
from model.cid import CID_SITE, CID_NOTE
from zweb.orm import ormiter
from model.zsite import Zsite
from model.site_po import po_cid_count_by_zsite_id

def can_rec_site_id_list():
    result = []
    for i in ormiter(Zsite, 'cid=%s'%CID_SITE):
        zsite_id = i.id
        count = po_cid_count_by_zsite_id(zsite_id, CID_NOTE)
        if count > 5:
            result.append(zsite_id)
    return set(result)

if __name__ == '__main__':
    result = []
    for z in Zsite.mc_get_list(can_rec_site_id_list()):
        result.append([z.id, z.name])
    writer = csv.writer(open('site_id_name.csv', 'wb'), quoting=csv.QUOTE_ALL)
    writer.writerows(result)
