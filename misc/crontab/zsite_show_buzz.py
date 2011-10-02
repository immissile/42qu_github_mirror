#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from zkit.single_process import single_process
from model.kv_misc import kv_int, KV_SHOW_BUZZ_POS
from model.zsite_list import ZsiteList
from model.buzz import buzz_show_new_all
from model.cid import CID_USER
@single_process
def buzz_show():
    prev_pos = kv_int.get(KV_SHOW_BUZZ_POS)
    #prev_pos = 3300
    c = ZsiteList.raw_sql('select max(id) from zsite_list')
    pos = c.fetchone()[0]
    #print pos,prev_pos
    if pos > prev_pos:
        c = ZsiteList.raw_sql(
            'select zsite_id from zsite_list where owner_id=0 and cid=%s and state=1 and id>%s and id<=%s order by id',
            CID_USER,
            prev_pos,
            pos
        )
        for zsite_id, in c.fetchall():
            #print zsite_id
            buzz_show_new_all(zsite_id)
        kv_int.set(KV_SHOW_BUZZ_POS, pos)

if __name__ == '__main__':
    buzz_show()

