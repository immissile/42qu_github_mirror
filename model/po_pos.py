#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time
from _db import cursor_by_table, Model, McModel, McLimitA, McCache
from po import Po

STATE_BUZZ = 1
STATE_MUTE = 0

class PoPos(Model):
    pass

mc_po_pos = McCache('PoPos.%s')

@mc_po_pos('{user_id}_{po_id}')
def po_pos_get(user_id, po_id):
    p = PoPos.get(user_id=user_id, po_id=po_id)
    if p:
        return p.pos
    return -1

mc_po_viewed_list = McLimitA('PoViewedList.%s', 128)

@mc_po_viewed_list('{po_id}')
def po_viewed_list(po_id, limit, offset):
    qs = PoPos.where(po_id=po_id).order_by('id desc')
    return [i.user_id for i in qs]

def po_buzz_list(po_id):
    qs = PoPos.where(po_id=po_id, state=STATE_BUZZ)
    return [i.user_id for i in qs]

def po_pos_set(user_id, po_id):
    po = Po.mc_get(po_id)
    pos = po.reply_id_last
    pos_old = po_pos_get(user_id, po_id)
    if pos > pos_old:
        PoPos.raw_sql('insert delayed into po_pos (user_id, po_id, pos, state) values (%s, %s, %s, %s) on duplicate key update pos=values(pos)', user_id, po_id, pos, STATE_MUTE)
        mc_po_pos.set('%s_%s' % (user_id, po_id), pos)
    if pos_old == -1:
        mc_po_viewed_list.delete(po_id)

def po_pos_state(user_id, po_id, state):
    pos = po_pos_get(user_id, po_id)
    if pos >= 0:
        p = PoPos.get(user_id=user_id, po_id=po_id)
        if p:
            p.state = state
            p.save()

if __name__ == '__main__':
    pass
