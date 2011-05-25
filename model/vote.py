#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McCacheA, McLimitA, McNum

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

UP_STATE = 1
MID_STATE = 0
DOWN_STATE = -1

class Vote(Model):
    pass

vote_up_count = McNum(lambda po_id: Vote.where(po_id=po_id, state=UP_STATE).count(), 'VoteUpCount.%s')
vote_down_count = McNum(lambda po_id: Vote.where(po_id=po_id, state=DOWN_STATE).count(), 'VoteDownCount.%s')

mc_vote_state = McCache('VoteState.%s')

@mc_vote_state('{user_id}_{po_id}')
def vote_state(user_id, po_id):
    v = Vote.get(user_id=user_id, po_id=po_id)
    if v:
        return v.state
    return 0

def _vote_up(user_id, po_id):
    Vote.raw_sql('insert into vote (user_id, po_id, state) values (%s, %s, 1) on duplicate key update state=1', user_id, po_id)

def _vote_mid(user_id, po_id):
    Vote.raw_sql('update vote set state=0 where user_id=%s and po_id=%s', user_id, po_id)

def _vote_down(user_id, po_id):
    Vote.raw_sql('insert into vote (user_id, po_id, state) values (%s, %s, -1) on duplicate key update state=-1', user_id, po_id)

def vote_up(user_id, po_id):
    state = vote_state(user_id, po_id)
    if state != 1:
        _vote_up(user_id, po_id)
        vote_mc_flush(user_id, po_id)
#    if state == 1:
#        return
#    elif state == 0:
#        rate_up_incr(po_id)
#    else:
#        rate_down2up(po_id)
#    _vote_up(user_id, po_id)

def vote_unup(user_id, po_id):
    state = vote_state(user_id, po_id)
    if state == 1:
        #rate_up_decr(po_id)
        _vote_mid(user_id, po_id)
        vote_mc_flush(user_id, po_id)

def vote_down(user_id, po_id):
    state = vote_state(user_id, po_id)
    if state != -1:
        _vote_down(user_id, po_id)
        vote_mc_flush(user_id, po_id)
#    if state == -1:
#        return
#    elif state == 0:
#        rate_down_incr(po_id)
#    else:
#        rate_up2down(po_id)
#    _vote_down(user_id, po_id)

def vote_undown(user_id, po_id):
    state = vote_state(user_id, po_id)
    if state == -1:
        #rate_down_decr(po_id)
        _vote_mid(user_id, po_id)
        vote_mc_flush(user_id, po_id)

def vote_mc_flush(user_id, po_id):
    mc_vote_state.delete('%s_%s' % (user_id, po_id))
    vote_up_count.delete(po_id)
    vote_down_count.delete(po_id)

if __name__ == '__main__':
    pass
