#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from _db import McModel, McCache, cursor_by_table, McCacheA, McCacheM
from cid import CID_PO


class SyncTurn(McModel):
    pass

def sync_state(user_id,cid):
    s = SyncTurn.get(zsite_id=user_id,cid=cid)
    if not s:
        SyncTurn.raw_sql('insert into sync_turn (zsite_id,cid,state) values(%s,%s,1)',user_id,cid)
        s = SyncTurn.get(zsite_id=user_id,cid=cid)
    return s.state


def sync_all(user_id):
    return [(cid,sync_state(user_id,cid)) for cid in CID_PO]

def sync_state_set(user_id,cid,state):
    state = int(bool(state))
    if state != sync_state(user_id,cid):
        SyncTurn.where(zsite_id=user_id,cid=cid).update(state=state)

