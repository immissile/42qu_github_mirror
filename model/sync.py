#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import McModel, McCache, cursor_by_table, McCacheA, McCacheM
from oauth_update import sync_by_oauth_id
from config import SITE_DOMAIN
from cid import CID_EVENT, CID_NOTE, CID_WORD, CID_AUDIO, CID_VIDEO, CID_PHOTO, CID_REVIEW
from zkit.txt import cnencut
from mq import mq_client
from model.zsite import Zsite
from oauth_follow import oauth_follow_by_oauth_id
from model.po import Po

mc_sync_state = McCache('SyncState:%s')
mc_sync_state_all = McCacheA('SyncStateAll:%s')

SYNC_CID_WORD = 1
SYNC_CID_NOTE = 2
SYNC_CID_EVENT = 3
SYNC_CID_SHARE = 4
SYNC_CID_REVIEW = 5

SYNC_CID_CN = (
    (SYNC_CID_WORD, '游吟碎语'),
    (SYNC_CID_NOTE, '文章影音'),
    (SYNC_CID_EVENT, '线下活动'),
    (SYNC_CID_SHARE, '推荐分享'),
    (SYNC_CID_REVIEW, '公司评价'),
)



SYNC_GET_CID = {
    CID_WORD: SYNC_CID_WORD,
    CID_NOTE: SYNC_CID_NOTE,
    CID_EVENT: SYNC_CID_EVENT,

    CID_AUDIO:SYNC_CID_NOTE,
    CID_VIDEO:SYNC_CID_NOTE,
    CID_PHOTO:SYNC_CID_NOTE,
    CID_REVIEW:SYNC_CID_REVIEW,
}

SYNC_CID_TXT = {
    CID_NOTE:'文章 : ',
    CID_EVENT:'发起活动 : ',
    CID_AUDIO:'音频 : ' ,
    CID_VIDEO:'视频 : ',
    CID_PHOTO:'图片 : ',
}

SYNC_CID = tuple(i[0] for i in SYNC_CID_CN)

class SyncTurn(McModel):
    pass

class SyncFollow(McModel):
    pass

def sync_follow_new(zsite_id, state, cid, txt, oauth_id=0):
    if txt:
        SyncFollow.raw_sql(
            'insert into sync_follow (zsite_id,state,cid,txt,oauth_id) values(%s,%s,%s,%s,%s) ',
             zsite_id, state, cid, txt, oauth_id
        )

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
    ).where('state>0').col_list(col='oauth_id')
    return s

def sync_po(po):
    id = po.user_id
    sync_cid = SYNC_GET_CID.get(po.cid)
    if not sync_cid:
        return
    for oauth_id in state_oauth_id_by_zsite_id_cid(id, sync_cid):
        sync_by_oauth_id(oauth_id, SYNC_CID_TXT.get(po.cid, '') + po.name_, 'http:%s'%po.link)


def sync_site_po(po, zsite):
    id = zsite.id

    user = Zsite.mc_get(po.user_id)
    if user:
        name = user.name
    else:
        name = None

    sync_cid = SYNC_GET_CID.get(po.cid)
    if not sync_cid:
        return
    txt = ''
    if po.cid in(CID_PHOTO, CID_VIDEO, CID_NOTE, CID_EVENT, CID_AUDIO):
        txt = po.txt
        if txt:
            txt = ' | %s'%po.txt

    for oauth_id in state_oauth_id_by_zsite_id_cid(id, sync_cid):
        sync_by_oauth_id(oauth_id, po.name_+txt, 'http:%s'%po.link, name)


def sync_join_event(id, event_id):
    po = Po.mc_get(event_id)
    s = state_oauth_id_by_zsite_id_cid(id, SYNC_CID_EVENT)
    for oauth_id in s:
        sync_by_oauth_id(oauth_id, '报名活动 : '+ po.name_, 'http:%s'%po.link)



def sync_recommend(id, po_id):
    from po import Po
    p = Po.mc_get(po_id)
    s = state_oauth_id_by_zsite_id_cid(id, SYNC_CID_SHARE)
    for oauth_id in s:
        rec_po = Po.mc_get(p.rid)
        if rec_po:
            txt = cnencut(p.name_, 20)
            if txt:
                txt = '%s -> '%txt
            else:
                txt = txt+"分享: "
            sync_by_oauth_id(oauth_id, txt + cnencut(rec_po.name_,50)  , 'http:%s'%rec_po.link)


def sync_follow_oauth_id_bind(user_id, cid, oauth_id):
    for pos, sync_follow in enumerate(
        SyncFollow.where(zsite_id=user_id, cid=cid, oauth_id=0)
    ):
        if pos:
            sync_follow.delete()

        sync_follow.oauth_id = oauth_id
        sync_follow.save()


def sync_follow(follow):
    oauth_id = follow.oauth_id
    sync_txt = follow.state&0b10

    if sync_txt:
        sync_by_oauth_id(
            oauth_id, follow.txt, 'http://%s'%SITE_DOMAIN
        )
    oauth_follow_by_oauth_id(oauth_id)

    follow.delete()




if __name__ == '__main__':
    #sync_po_by_zsite_id(10076346, 10076346)
    pass
