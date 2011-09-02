#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from _db import McModel, McCache, cursor_by_table, McCacheA, McCacheM
from oauth_update import sync_by_oauth_id
from oauth import OauthToken
from config import SITE_DOMAIN
from cid import CID_EVENT, CID_NOTE, CID_WORD
from mq import mq_client
from oauth_follow import oauth_follow_by_oauth_id

mc_sync_state = McCache('SyncState:%s')
mc_sync_state_all = McCacheA('SyncStateAll:%s')

SYNC_CID_WORD = 1
SYNC_CID_NOTE = 2
SYNC_CID_EVENT = 3
SYNC_CID_SHARE = 4


SYNC_CID_CN = (
    (SYNC_CID_WORD, '游吟碎语'),
    (SYNC_CID_NOTE, '撰写文章'),
    (SYNC_CID_EVENT, '线下活动'),
    (SYNC_CID_SHARE, '推荐分享'),
)



SYNC_GET_CID = {
    CID_WORD: SYNC_CID_WORD,
    CID_NOTE: SYNC_CID_NOTE,
    CID_EVENT: SYNC_CID_EVENT,
}

SYNC_CID_TXT = (
    '',
    '文章 : ',
    '发起活动 :',
    '分享 : ',
)

SYNC_CID = tuple(i[0] for i in SYNC_CID_CN)

class SyncTurn(McModel):
    pass

class SyncFollow(McModel):
    pass

def sync_follow_new(zsite_id, state, cid, txt):
    SyncFollow.raw_sql('insert into sync_follow (id,state,cid,txt) values(%s,%s,%s,%s) on duplicate key update id=id', zsite_id, state, cid, txt)

@mc_sync_state('{user_id}_{oauth_id}_{cid}')
def sync_state(user_id, oauth_id, cid):
    s = SyncTurn.get(zsite_id=user_id, cid=cid, oauth_id=oauth_id)
    if not s:
        SyncTurn.raw_sql('insert into sync_turn (zsite_id,cid,state, oauth_id) values(%s,%s,1,%s)', user_id, cid, oauth_id)
        s = SyncTurn.get(zsite_id=user_id, cid=cid, oauth_id=oauth_id)
    return s.state

@mc_sync_state_all('{user_id}_{oauth_id}')
def sync_all(user_id, oauth_id):
    return [sync_state(user_id, oauth_id, cid) for cid in SYNC_CID]

def sync_state_set(user_id, cid, state, oauth_id):
    state = int(bool(state))
    if state != sync_state(user_id, oauth_id, cid):
        SyncTurn.where(zsite_id=user_id, cid=cid, oauth_id=oauth_id).update(state=state)
        mc_sync_state.set('%s_%s_%s'%(user_id, oauth_id, cid), state)
        mc_sync_state_all.delete('%s_%s'%(user_id, oauth_id))


def state_oauth_id_by_zsite_id_cid(zsite_id, cid):
    s = SyncTurn.where(
        zsite_id=zsite_id, cid=cid
    ).where('state>0').col_list('oauth_id')
    return s

def sync_po(po):
    id = po.user_id
    cid = SYNC_GET_CID[p.cid]
    for oauth_id in state_oauth_id_by_zsite_id_cid(id, cid):
        sync_by_oauth_id(oauth_id, SYNC_CID_TXT[cid-1] + p.name_, 'http:%s'%p.link)

def sync_join_event(id, po):
    s = state_oauth_id_by_zsite_id_cid(id, SYNC_CID_EVENT)
    for oauth_id in s:
        sync_by_oauth_id(oauth_id, '报名活动 : '+ po.name_, 'http:%s'%po.link)

def sync_recommend_by_zsite_id(id, po_id, cid=4):
    from po import Po
    cid = int(cid)
    p = Po.mc_get(po_id)
    s = SyncTurn.raw_sql('select state,oauth_id from sync_turn where zsite_id = %s and cid = %s', id, cid).fetchall()
    if s:
        for state, oauth_id in s:
            if state:
                sync_by_oauth_id(oauth_id, SYNC_CID_TXT[cid-1] + p.name_, 'http:%s'%p.link)




def sync_follow_by_sync_id(zsite_id, oauth_id):
    s = SyncFollow.get(zsite_id)
    if s:
        a, b = divmod(s.state, 2)
        if a:
            sync_by_oauth_id(oauth_id, s.txt, "http://%s"%SITE_DOMAIN)
        if b:
            oauth_follow_by_oauth_id(oauth_id)
        s.delete()


#mq_sync_po_by_zsite_id = mq_client(sync_po_by_zsite_id)
#mq_sync_join_event_by_zsite_id = mq_client(sync_join_event_by_zsite_id)
#mq_sync_recommend_by_zsite_id = mq_client(sync_recommend_by_zsite_id)
#mq_sync_follow_by_sync_id = mq_client(sync_follow_by_sync_id)


if __name__ == '__main__':
    pass
    sync_po_by_zsite_id(10076346, 10076346)
