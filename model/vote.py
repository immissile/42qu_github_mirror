#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McCacheA, McLimitA, McNum
from feed import mc_feed_tuple

STATE_UP = 1
STATE_0 = 0
STATE_DOWN = -1

class Vote(Model):
    pass

vote_up_count = McNum(lambda po_id: Vote.where(po_id=po_id, state=STATE_UP).count(), 'VoteUpCount:%s')
vote_down_count = McNum(lambda po_id: Vote.where(po_id=po_id, state=STATE_DOWN).count(), 'VoteDownCount:%s')
vote_count = McNum(lambda po_id: vote_up_count(po_id) - vote_down_count(po_id) , 'VoteCount:%s')

mc_vote_state = McCache('VoteState.%s')

@mc_vote_state('{user_id}_{po_id}')
def _vote_state(user_id, po_id):
    v = Vote.get(user_id=user_id, po_id=po_id)
    if v:
        return v.state
    return 0

def vote_state(user_id, po_id):
    if not user_id:
        return 0
    return _vote_state(user_id, po_id)

def _vote_up(user_id, po_id):
    Vote.raw_sql('insert into vote (user_id, po_id, state) values (%s, %s, 1) on duplicate key update state=1', user_id, po_id)

def _vote_0(user_id, po_id):
    Vote.raw_sql('update vote set state=0 where user_id=%s and po_id=%s', user_id, po_id)

def _vote_down(user_id, po_id):
    Vote.raw_sql('insert into vote (user_id, po_id, state) values (%s, %s, -1) on duplicate key update state=-1', user_id, po_id)


def vote_up(user_id, po_id):
    state = vote_state(user_id, po_id)
    if state != STATE_UP:
        _vote_up(user_id, po_id)
        vote_mc_flush(user_id, po_id)

def vote_up_x(user_id, po_id):
    state = vote_state(user_id, po_id)
    if state == STATE_UP:
        _vote_0(user_id, po_id)
        vote_mc_flush(user_id, po_id)

def vote_down(user_id, po_id):
    state = vote_state(user_id, po_id)
    if state != STATE_DOWN:
        _vote_down(user_id, po_id)
        vote_mc_flush(user_id, po_id)

def vote_down_x(user_id, po_id):
    state = vote_state(user_id, po_id)
    if state == STATE_DOWN:
        _vote_0(user_id, po_id)
        vote_mc_flush(user_id, po_id)

mc_vote_user_id_list = McLimitA('VoteUserIdList.%s', 128)

@mc_vote_user_id_list('{po_id}')
def vote_user_id_list(po_id, limit, offset):
    return Vote.where(po_id=po_id, state=STATE_UP).order_by('id desc').col_list(limit, offset, 'user_id')

def vote_mc_flush(user_id, po_id):
    mc_vote_state.delete('%s_%s' % (user_id, po_id))
    po_id = str(po_id)
    vote_up_count.delete(po_id)
    vote_down_count.delete(po_id)
    vote_count.delete(po_id)
    mc_vote_user_id_list.delete(po_id)
    mc_feed_tuple.delete(po_id)
    from rank import rank_update
    rank_update(po_id)

if __name__ == '__main__':
    pass
#class Rate(Model):
#    pass
#
#mc_rate_tuple = McCacheA('RateTuple.%s')
#
#@mc_rate_tuple('{po_id}')
#def rate_tuple(po_id):
#    r = Rate.get(po_id)
#    if r:
#        return r.up, r.down
#    return 0, 0
#
#def rate_up_incr(po_id):
#    Rate.raw_sql('insert into rate (id, up) values (%s, 1) on duplicate key update up=up+1', po_id)
#
#def rate_up_decr(po_id):
#    Rate.raw_sql('update rate set up=up-1 where id=%s', po_id)
#
#def rate_down_incr(po_id):
#    Rate.raw_sql('insert into rate (id, down) values (%s, 1) on duplicate key update down=down+1', po_id)
#
#def rate_down_decr(po_id):
#    Rate.raw_sql('update rate set down=down-1 where id=%s', po_id)
#
#def rate_up2down(po_id):
#    Rate.raw_sql('update rate set up=up-1 and down=down+1 where id=%s', po_id)
#
#def rate_down2up(po_id):
#    Rate.raw_sql('update rate set up=up+1 and down=down-1 where id=%s', po_id)
