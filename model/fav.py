#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McCacheA, McLimitA, McNum
from po import Po

class Fav(Model):
    pass

mc_fav_state = McCache('FavState.%s')

@mc_fav_state('{user_id}_{po_id}')
def fav_state(user_id, po_id):
    if Fav.get(user_id=user_id, po_id=po_id):
        return 1
    return 0

def fav_add(user_id, po_id):
    if not fav_state(user_id, po_id):
        Fav(user_id=user_id, po_id=po_id).save()
        mc_fav_state.set('%s_%s' % (user_id, po_id), 1)

def fav_rm(user_id, po_id):
    if fav_state(user_id, po_id):
        Fav.where(user_id=user_id, po_id=po_id).delete()
        mc_fav_state.set('%s_%s' % (user_id, po_id), 0)

def fav_rm_by_po_id(po_id):
    for i in Fav.where(po_id=po_id):
        i.delete()
        user_id = i.user_id
        mc_fav_po_id_list_by_user_id.delete(user_id)
        mc_fav_state.delete('%s_%s' % (user_id, po_id))

mc_fav_po_id_list_by_user_id = McLimitA('FavPoIdListByUserId.%s', 128)

@mc_fav_po_id_list_by_user_id('{user_id}')
def fav_po_id_list_by_user_id(user_id, limit, offset):
    return Fav.where(user_id=user_id).order_by('id desc').col_list(limit, offset)

def fav_po_list_by_user_id(user_id, limit, offset):
    id_list = fav_po_id_list_by_user_id(user_id, limit, offset)
    return Po.mc_get_list(id_list)

if __name__ == '__main__':
    pass
