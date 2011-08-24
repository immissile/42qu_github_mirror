#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from _db import McModel, McCache, cursor_by_table, McCacheA, McCacheM
from cid import CID_PO
from po import Po
from oauth_update import sync_by_oauth_id
from oauth import OauthToken

class SyncTurn(McModel):
    pass

class SyncFollow(McModel):
    pass

def sync_follow_new(zsite_id, state, cid, txt):
    SyncFollow.raw_sql('insert into sync_follow (zsite_id,state,cid,txt) values(%s,%s,%s,%s)', zsite_id, state, cid, txt)

def sync_state(user_id, cid):
    s = SyncTurn.get(zsite_id=user_id, cid=cid)
    if not s:
        SyncTurn.raw_sql('insert into sync_turn (zsite_id,cid,state) values(%s,%s,1)', user_id, cid)
        s = SyncTurn.get(zsite_id=user_id, cid=cid)
    return s.state


def sync_all(user_id):
    return [(cid, sync_state(user_id, cid)) for cid in CID_PO]

def sync_state_set(user_id, cid, state):
    state = int(bool(state))
    if state != sync_state(user_id, cid):
        SyncTurn.where(zsite_id=user_id, cid=cid).update(state=state)

def sync_by_po_id(id):
    p = Po.get(id)
    user_id = p.user_id
    cid = p.cid
    s = SyncTurn.raw_sql('select cid,state from sync_turn where zsite_id = %s', user_id).fetchall()
    o = OauthToken.raw_sql('select id from oauth_token where zsite_id = %s', user_id).fetchall()
    if s:
        for scid, state in s:
            if cid == scid and state:
                for oid in o:
                    sync_by_oauth_id(oid[0], p.name_, 'http://%s.42qu.com/%s'%(p.user_id, p.id))



def sync_follow_by_sync_id(id):
    s = SyncFollow.get(id)
    user_id = s.zsite_id
    o = OauthToken.raw_sql('select id from oauth_token where zsite_id = %s', user_id).fetchall()
    if s.state:
        if s.state >= 2:
            for oid in o:
                sync_by_oauth_id(oid[0], s.txt, 'http://42qu.com')
        else:
            oauth_follow_by_oauth_id(oid[0])




if __name__ == '__main__':
    sync_by_po_id(10043539)

