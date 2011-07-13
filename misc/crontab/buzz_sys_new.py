#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from zkit.single_process import single_process
from model.kv_misc import kv_int, KV_BUZZ_SYS_POS
from model.buzz_sys import BuzzSys
from model.buzz import buzz_sys_new_all

@single_process
def buzz_sys():
    prev_pos = kv_int.get(KV_BUZZ_SYS_POS)
    c = BuzzSys.raw_sql('select max(id) from buzz_sys')
    pos = c.fetchone()[0]
    if pos > prev_pos:
        c = BuzzSys.raw_sql('select id from buzz_sys where seq=0 and id>%s and id<=%s order by id', prev_pos, pos)
        for id, in c.fetchall():
            buzz_sys_new_all(id)
        kv_int.set(KV_BUZZ_SYS_POS, pos)

if __name__ == '__main__':
    buzz_sys()
