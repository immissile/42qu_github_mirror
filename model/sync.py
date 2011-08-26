#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from _db import McModel, McCache, cursor_by_table, McCacheA, McCacheM
from po import Po
from oauth_update import sync_by_oauth_id
from oauth import OauthToken
from model.cid import CID_EVENT, CID_NOTE, CID_WORD
mc_sync_state = McCache('SyncState:%s')
mc_sync_state_all = McCacheA('SyncStateAll:%s')

SYNC_CID_CN = (
    (1, '游吟碎语'),
    (2, '撰写文章'),
    (3, '线下活动'),
    (4, '推荐分享'),
)
SYNC_GET_CID = {
       CID_WORD :'1',
       CID_NOTE :'2',
       CID_EVENT :'3',
        }

SYNC_CID = tuple(i[0] for i in SYNC_CID_CN)

class SyncTurn(McModel):
    pass

class SyncFollow(McModel):
    pass

def sync_follow_new(zsite_id, state, cid, txt):
    SyncFollow.raw_sql('insert into sync_follow (zsite_id,state,cid,txt) values(%s,%s,%s,%s)', zsite_id, state, cid, txt)

@mc_sync_state('{user_id}_{cid}')
def sync_state(user_id, oauth_id, cid):
    s = SyncTurn.get(zsite_id=user_id, cid=cid)
    if not s:
        SyncTurn.raw_sql('insert into sync_turn (zsite_id,cid,state, oauth_id) values(%s,%s,1,%s)', user_id, cid,oauth_id)
        s = SyncTurn.get(zsite_id=user_id, cid=cid)
    return s.state

@mc_sync_state_all("{user_id}")
def sync_all(user_id,oauth_id):
    return [sync_state(user_id,oauth_id, cid) for cid in SYNC_CID]

def sync_state_set(user_id, cid, state, oauth_id):
    state = int(bool(state))
    if state != sync_state(user_id, oauth_id, cid):
        SyncTurn.where(zsite_id=user_id, cid=cid).update(state=state)
        mc_sync_state.set('%s_%s'%(user_id, cid), state)
        mc_sync_state_all.delete(user_id)

def sync_by_po_id(id):
    p = Po.get(id)
    user_id = p.user_id
    cid = p.cid
    s = SyncTurn.raw_sql('select cid,state,oauth_id from sync_turn where zsite_id = %s', user_id).fetchall()
    if s:
        for scid, state, oauth_id in s:
            if state and SYNC_GET_CID.get(cid):
                sync_by_oauth_id(oauth_id, p.name_, 'http://%s.42qu.com/%s'%(p.user_id, p.id))



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

