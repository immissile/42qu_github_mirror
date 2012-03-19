#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from zkit.single_process import single_process
from model.kv_misc import kv_int, KV_NOTICE_POS
from model.cid import CID_NOTICE_WALL, CID_MAIL_DAY
from model.state import STATE_APPLY
from model.notice import Notice, notice_mail_day, NOTICE_MAIL_DAY
from model.mail_notice import mail_notice_state
from time import time, sleep
from zkit.orderedset import OrderedSet
from collections import defaultdict
from model.days import today_seconds




@single_process
def notice_day():
    prev_pos = kv_int.get(KV_NOTICE_POS)
    c = Notice.raw_sql(
        'select max(id) from notice where create_time<%s', today_seconds()
    )
    pos = c.fetchone()[0]
    if pos > prev_pos:
        d = defaultdict(OrderedSet)

        for i in Notice.where(state=STATE_APPLY).where(
            'id>%s and id<=%s', prev_pos, pos
        ):
            cid = i.cid
            to_id = i.to_id
            if cid in NOTICE_MAIL_DAY and mail_notice_state(to_id, CID_MAIL_DAY):
                d[to_id].add((i.from_id, cid, i.rid))

        for to_id, li in d.iteritems():
            notice_mail_day(to_id, li)
            sleep(0.1)

        kv_int.set(KV_NOTICE_POS, pos)



if __name__ == '__main__':
    notice_day()
