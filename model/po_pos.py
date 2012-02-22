#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time
from _db import cursor_by_table, Model, McModel, McLimitA, McCache, McCacheA, McCacheM, redis
from po import Po

STATE_BUZZ = 1
STATE_MUTE = 0

class PoPos(Model):
    pass

mc_po_pos = McCacheM('PoPos.%s')

def user_id_list_by_po_pos_buzz(po_id):
    return set(
        PoPos.where(
            po_id=po_id, state=STATE_BUZZ
        ).col_list(col="user_id")
    )


def po_pos_get_last_reply_id(user_id, po_id):
    return po_pos_get(user_id, po_id)[0]

@mc_po_pos('{user_id}_{po_id}')
def po_pos_get(user_id, po_id):
    p = PoPos.get(user_id=user_id, po_id=po_id)
    if p:
        return p.pos, p.state
    return -1, STATE_MUTE

mc_po_viewed_list = McLimitA('PoViewedList.%s', 128)

@mc_po_viewed_list('{po_id}')
def po_viewed_list(po_id, limit, offset):
    qs = PoPos.where(po_id=po_id).order_by('id desc')
    return [i.user_id for i in qs]

def po_buzz_list(po_id):
    qs = PoPos.where(po_id=po_id, state=STATE_BUZZ)
    return [i.user_id for i in qs]

def po_pos_mark(user_id, po):
    _po_pos(
        user_id, po, STATE_MUTE, 
        'insert delayed into po_pos (user_id, po_id, pos, state) values (%s, %s, %s, %s) on duplicate key update pos=values(pos)'
    )

def po_pos_set(user_id, po):
    _po_pos(
        user_id, po, STATE_BUZZ, 
        'insert delayed into po_pos (user_id, po_id, pos, state) values (%s, %s, %s, %s) on duplicate key update pos=values(pos), state=values(state)'
    )

def _po_pos(user_id, po, state, sql):
    pos = po.reply_id_last
    po_id = po.id
    pos_old, _ = po_pos_get(user_id, po_id)
    print pos_old
    if pos_old == -1:
        from po_tag import REDIS_FEED_PO_VIEWED_COUNT, section_rank_refresh
        redis.hincrby(REDIS_FEED_PO_VIEWED_COUNT, po.id, 1)
        section_rank_refresh(po)
    if pos > pos_old:
        PoPos.raw_sql(
            sql,
            user_id, po_id, pos, state 
        )
        mc_po_pos.delete('%s_%s' % (user_id, po_id))

        from buzz_reply import buzz_reply_hide
        buzz_reply_hide(user_id, po_id)

    if pos_old == -1:
        mc_po_viewed_list.delete(po_id)


def po_pos_set_by_po_id(user_id, po_id):
    if user_id:
        po = Po.mc_get(po_id)
        if po:
            po_pos_set(user_id, po)

def po_pos_state_buzz(user_id, po):
    po_id = po.id
    if not po_pos_state(user_id, po_id, STATE_BUZZ):
        po_pos_set(user_id, po)

def po_pos_state_mute(user_id, po_id):
    po_pos_state(user_id, po_id, STATE_MUTE)

def po_pos_state(user_id, po_id, state):
    pos, state_old = po_pos_get(user_id, po_id)
    if pos >= 0 and state_old != state:
        PoPos.raw_sql('update po_pos set state=%s where user_id=%s and po_id=%s', state, user_id, po_id)
        mc_po_pos.delete('%s_%s' % (user_id, po_id))
        return True

if __name__ == '__main__':
    pass
    po = Po.get(517)
    print po_pos_get(10000000, po.id)
    print po_pos_get(10000000, po.id)
    po_pos_set(10000000, po)
    print po_pos_get(10000000, po.id)
    print po_pos_get(10000000, po.id)
