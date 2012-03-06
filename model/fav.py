#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McCacheA, McLimitA, McNum
from po import Po, PO_SHARE_FAV_CID
from event import Event
from state import STATE_RM, STATE_SECRET, STATE_ACTIVE
from cid import CID_EVENT
from model.po_pos import po_pos_get, po_pos_set, po_pos_state, STATE_BUZZ
from zsite import Zsite
from collections import defaultdict
from model.buzz import mq_buzz_po_fav_new

class Fav(Model):
    pass

mc_fav_cid = McCache('FavCid.%s')

@mc_fav_cid('{user_id}_{po_id}')
def fav_cid(user_id, po_id):
    f = Fav.get(user_id=user_id, po_id=po_id)
    if f:
        return f.cid
    return 0

def fav_cid_dict(user_id, po_id_list):
    if not user_id:
        return defaultdict(int)
    arg_list = tuple((user_id, i) for i in po_id_list)
    key_dict = dict(('%s_%s' % (user_id, i), i) for i in po_id_list)
    t = mc_fav_cid.get_dict(key_dict)
    d = {}
    for k, v in key_dict.iteritems():
        cid = t[k]
        if cid is None:
            cid = fav_cid(user_id, v)
        d[v] = cid
    return d

def fav_new(user_id, po_id):
    po = Po.mc_get(po_id)
    if po and po.cid in PO_SHARE_FAV_CID and po.state >= STATE_ACTIVE and not fav_cid(user_id, po_id):
        cid = po.cid
        Fav(user_id=user_id, po_id=po_id, cid=cid).save()
        mc_fav_cid.set('%s_%s' % (user_id, po_id), cid)
        mc_flush_by_user_id(user_id, cid)
        mc_flush_by_po_id(po_id)
        po_pos_set(user_id, po)

        from po_tag import po_score_incr
        po_score_incr(po, user_id, 7)

        mq_buzz_po_fav_new(user_id, po_id)

def fav_rm(user_id, po_id):
    cid = fav_cid(user_id, po_id)
    if cid:
        Fav.where(user_id=user_id, po_id=po_id).delete()
        mc_fav_cid.set('%s_%s' % (user_id, po_id), 0)
        mc_flush_by_user_id(user_id, cid)
        mc_flush_by_po_id(po_id)
        
        from po_tag import po_score_incr
        po_score_incr(po, user_id, -7)

def fav_rm_by_po(po):
    po_id = po.id
    cid = po.cid
    for i in Fav.where(po_id=po_id):
        i.delete()
        user_id = i.user_id
        mc_fav_cid.delete('%s_%s' % (user_id, po_id))
        mc_flush_by_user_id(user_id, cid)
    mc_flush_by_po_id(po_id)

def mc_flush_by_user_id(user_id, cid):
    key = '%s_%s' % (user_id, cid)
    mc_fav_po_id_list_by_user_id_cid.delete(key)
    fav_po_count_by_user_id_cid.delete(key)
    fav_po_count_by_user_id.delete(user_id)

def mc_flush_by_po_id(po_id):
    mc_fav_user_id_list_by_po_id.delete(po_id)
    fav_user_count_by_po_id.delete(po_id)

mc_fav_po_id_list_by_user_id_cid = McLimitA('FavPoIdListByUserIdCid.%s', 128)

fav_po_count_by_user_id_cid = McNum(lambda user_id, cid: Fav.where(user_id=user_id, cid=cid).count(), 'FavPoCountByUserIdCid.%s')

fav_po_count_by_user_id = McNum(lambda user_id: Fav.where(user_id=user_id).count(), 'FavPoCountByUserId.%s')

@mc_fav_po_id_list_by_user_id_cid('{user_id}_{cid}')
def fav_po_id_list_by_user_id_cid(user_id, cid, limit, offset):
    return Fav.where(user_id=user_id, cid=cid).order_by('id desc').col_list(limit, offset, 'po_id')

def fav_po_list_by_user_id_cid(user_id, cid, limit, offset=0):
    id_list = fav_po_id_list_by_user_id_cid(user_id, cid, limit, offset)
    if cid == CID_EVENT:
        return zip(Event.mc_get_list(id_list), Po.mc_get_list(id_list))
    return Po.mc_get_list(id_list)


mc_fav_user_id_list_by_po_id = McLimitA('FavUserIdListByPoId.%s', 128)

fav_user_count_by_po_id = McNum(lambda po_id: Fav.where(po_id=po_id).count(), 'FavUserCountByPoId.%s')

@mc_fav_user_id_list_by_po_id('{po_id}')
def fav_user_id_list_by_po_id(po_id, limit, offset):
    return Fav.where(po_id=po_id).order_by('id desc').col_list(limit, offset, 'user_id')

def fav_user_list_by_po_id(po_id, limit, offset=0):
    id_list = fav_user_id_list_by_po_id(po_id, limit, offset)
    return Zsite.mc_get_list(id_list)


if __name__ == '__main__':
    fav_new(10000212, 10071341)
