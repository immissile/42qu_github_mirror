#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from model.notice import Notice, STATE_GTE_APPLY, notice_id_count
from model.cid import CID_NOTICE_WALL, CID_NOTICE_WALL_REPLY

def rm_reduplicate():
    a = set()
    for i in Notice.where('cid in (%s, %s)' % (CID_NOTICE_WALL, CID_NOTICE_WALL_REPLY)).where(STATE_GTE_APPLY).order_by('id desc'):
        from_id = i.from_id
        to_id = i.to_id
        cid = i.cid
        rid = i.rid
        t = (from_id, to_id, cid, rid)
        if t not in a:
            if notice_id_count(*t):
                a.add(t)

    for from_id, to_id, cid, rid in a:
        for seq, i in enumerate(Notice.where(from_id=from_id, to_id=to_id, cid=cid, rid=rid).order_by('id desc')):
            if seq:
                i.rm(to_id)

if __name__ == '__main__':
    rm_reduplicate()
