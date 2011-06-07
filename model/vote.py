#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McCacheA, McLimitA, McNum

STATE_INCR = 1
STATE_0 = 0
STATE_DECR = -1

class Vote(Model):
    pass

vote_incr_count = McNum(lambda feed_id: Vote.where(feed_id=feed_id, state=STATE_INCR).count(), 'VoteIncrCount.%s')
vote_decr_count = McNum(lambda feed_id: Vote.where(feed_id=feed_id, state=STATE_DECR).count(), 'VoteDecrCount.%s')

mc_vote_state = McCache('VoteState.%s')

@mc_vote_state('{user_id}_{feed_id}')
def vote_state(user_id, feed_id):
    v = Vote.get(user_id=user_id, feed_id=feed_id)
    if v:
        return v.state
    return 0

def _vote_incr(user_id, feed_id):
    Vote.raw_sql('insert into vote (user_id, feed_id, state) values (%s, %s, 1) on duplicate key update state=1', user_id, feed_id)

def _vote_0(user_id, feed_id):
    Vote.raw_sql('update vote set state=0 where user_id=%s and feed_id=%s', user_id, feed_id)

def _vote_decr(user_id, feed_id):
    Vote.raw_sql('insert into vote (user_id, feed_id, state) values (%s, %s, -1) on duplicate key update state=-1', user_id, feed_id)

def vote_incr(user_id, feed_id):
    state = vote_state(user_id, feed_id)
    if state != STATE_INCR:
        _vote_incr(user_id, feed_id)
        vote_mc_flush(user_id, feed_id)

def vote_incr_x(user_id, feed_id):
    state = vote_state(user_id, feed_id)
    if state == STATE_INCR:
        _vote_0(user_id, feed_id)
        vote_mc_flush(user_id, feed_id)

def vote_decr(user_id, feed_id):
    state = vote_state(user_id, feed_id)
    if state != STATE_DECR:
        _vote_decr(user_id, feed_id)
        vote_mc_flush(user_id, feed_id)

def vote_decr_x(user_id, feed_id):
    state = vote_state(user_id, feed_id)
    if state == STATE_DECR:
        _vote_0(user_id, feed_id)
        vote_mc_flush(user_id, feed_id)

def vote_mc_flush(user_id, feed_id):
    mc_vote_state.delete('%s_%s' % (user_id, feed_id))
    vote_incr_count.delete(feed_id)
    vote_decr_count.delete(feed_id)

if __name__ == '__main__':
    pass

#class Rate(Model):
#    pass
#
#mc_rate_tuple = McCacheA('RateTuple.%s')
#
#@mc_rate_tuple('{feed_id}')
#def rate_tuple(feed_id):
#    r = Rate.get(feed_id)
#    if r:
#        return r.up, r.down
#    return 0, 0
#
#def rate_incr_incr(feed_id):
#    Rate.raw_sql('insert into rate (id, up) values (%s, 1) on duplicate key update up=up+1', feed_id)
#
#def rate_incr_decr(feed_id):
#    Rate.raw_sql('update rate set up=up-1 where id=%s', feed_id)
#
#def rate_decr_incr(feed_id):
#    Rate.raw_sql('insert into rate (id, down) values (%s, 1) on duplicate key update down=down+1', feed_id)
#
#def rate_decr_decr(feed_id):
#    Rate.raw_sql('update rate set down=down-1 where id=%s', feed_id)
#
#def rate_incr2down(feed_id):
#    Rate.raw_sql('update rate set up=up-1 and down=down+1 where id=%s', feed_id)
#
#def rate_decr2up(feed_id):
#    Rate.raw_sql('update rate set up=up+1 and down=down-1 where id=%s', feed_id)

