#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McCacheA, McLimitA, McNum
from po import Po

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

def fav_add(user_id, po_id):
    po = Po.mc_get(po_id)
    if po and not fav_cid(user_id, po_id):
        cid = po.cid
        Fav(user_id=user_id, po_id=po_id, cid=cid).save()
        mc_fav_cid.set('%s_%s' % (user_id, po_id), cid)

def fav_rm(user_id, po_id):
    cid = fav_cid(user_id, po_id)
    if cid:
        Fav.where(user_id=user_id, po_id=po_id).delete()
        mc_fav_cid.set('%s_%s' % (user_id, po_id), 0)
        mc_fav_po_id_list_by_user_id_cid.delete('%s_%s' % (user_id, cid))

def fav_rm_by_po_id(po_id, cid):
    for i in Fav.where(po_id=po_id):
        i.delete()
        user_id = i.user_id
        mc_fav_cid.delete('%s_%s' % (user_id, po_id))
        mc_fav_po_id_list_by_user_id_cid.delete('%s_%s' % (user_id, cid))

mc_fav_po_id_list_by_user_id_cid = McLimitA('FavPoIdListByUserIdCid.%s', 128)

@mc_fav_po_id_list_by_user_id_cid('{user_id}_{cid}')
def fav_po_id_list_by_user_id_cid(user_id, cid, limit, offset):
    return Fav.where(user_id=user_id, cid=cid).order_by('id desc').col_list(limit, offset)

def fav_po_list_by_user_id_cid(user_id, cid, limit, offset):
    id_list = fav_po_id_list_by_user_id_cid(user_id, cid, limit, offset)
    return Po.mc_get_list(id_list)

if __name__ == '__main__':
    print fav_cid_dict(10000212, [1,3,4])
