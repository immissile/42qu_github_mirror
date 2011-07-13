#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from zkit.single_process import single_process
from model.kv_misc import kv_int, KV_NOTICE_POS
from model.cid import CID_INVITE_QUESTION
from model.state import STATE_APPLY
from model.notice import Notice, notice_mail
from time import time, sleep

@single_process
def notice_me():
    prev_pos = kv_int.get(KV_NOTICE_POS)
    c = Notice.raw_sql('select max(id) from notice where create_time<%s', int(time()) - 3600 * 12)
    pos = c.fetchone()[0]
    if pos > prev_pos:
        for i in Notice.where(state=STATE_APPLY).where('id>%s and id<=%s', prev_pos, pos):
            notice_mail(i)
            sleep(1)
        kv_int.set(KV_NOTICE_POS, pos)

if __name__ == '__main__':
    notice_me()
