#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from zkit.single_process import single_process
from model.kv_misc import kv_int, KV_BUZZ_FOLLOW_POS
from model.cid import CID_BUZZ_FOLLOW
from model.buzz import Buzz, buzz_pos
from model.mail_notice import mail_notice_state
from time import time, sleep
from zkit.orderedset import OrderedSet
from collections import defaultdict


@single_process
def buzz_follow_mail():
    prev_pos = kv_int.get(KV_BUZZ_FOLLOW_POS)
    c = Buzz.raw_sql(
        'select max(id) from buzz where create_time<%s', int(time()) - 60 * 20
    )
    pos = c.fetchone()[0]
    if pos > prev_pos:
        d = defaultdict(list)
        d2 = {}

        for i in Buzz.where(cid=CID_BUZZ_FOLLOW).where('to_id=rid').where(
            'id>%s and id<=%s', prev_pos, pos
        ):
            id = i.id
            d[i.to_id].append(id)
            d2[id] = i.from_id

        d3 = defaultdict(OrderedSet)
        for to_id, li in d.iteritems():
            min_id = buzz_pos.get(to_id)
            for id in li:
                if id > min_id:
                    d3[to_id].add(d2[id])

        for to_id, li in d3.iteritems():
            for from_id in li:
                print from_id, to_id
                #follow_mail_new(from_id, to_id)
                sleep(0.1)

        kv_int.set(KV_BUZZ_FOLLOW_POS, pos)


if __name__ == '__main__':
    buzz_follow_mail()
