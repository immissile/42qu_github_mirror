#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McCacheA, McLimitA, McNum
from feed import mc_feed_tuple

STATE_UP = 1
STATE_0 = 0
STATE_DOWN = -1

class Vote(Model):
    pass

vote_up_count = McNum(lambda feed_id: Vote.where(feed_id=feed_id, state=STATE_UP).count(), 'VoteUpCount:%s')
vote_down_count = McNum(lambda feed_id: Vote.where(feed_id=feed_id, state=STATE_DOWN).count(), 'VoteDownCount:%s')
vote_count = McNum(lambda feed_id: vote_up_count(feed_id) - vote_down_count(feed_id) , 'VoteCount:%s')

mc_vote_state = McCache('VoteState.%s')

@mc_vote_state('{user_id}_{feed_id}')
def _vote_state(user_id, feed_id):
    v = Vote.get(user_id=user_id, feed_id=feed_id)
    if v:
        return v.state
    return 0

def vote_state(user_id, feed_id):
    if not user_id:
        return 0
    return _vote_state(user_id, feed_id)

def _vote_up(user_id, feed_id):
    Vote.raw_sql('insert into vote (user_id, feed_id, state) values (%s, %s, 1) on duplicate key update state=1', user_id, feed_id)

def _vote_0(user_id, feed_id):
    Vote.raw_sql('update vote set state=0 where user_id=%s and feed_id=%s', user_id, feed_id)

def _vote_down(user_id, feed_id):
    Vote.raw_sql('insert into vote (user_id, feed_id, state) values (%s, %s, -1) on duplicate key update state=-1', user_id, feed_id)


def vote_up(user_id, feed_id):
    state = vote_state(user_id, feed_id)
    if state != STATE_UP:
        _vote_up(user_id, feed_id)
        vote_mc_flush(user_id, feed_id)

def vote_up_x(user_id, feed_id):
    state = vote_state(user_id, feed_id)
    if state == STATE_UP:
        _vote_0(user_id, feed_id)
        vote_mc_flush(user_id, feed_id)

def vote_down(user_id, feed_id):
    state = vote_state(user_id, feed_id)
    if state != STATE_DOWN:
        _vote_down(user_id, feed_id)
        vote_mc_flush(user_id, feed_id)

def vote_down_x(user_id, feed_id):
    state = vote_state(user_id, feed_id)
    if state == STATE_DOWN:
        _vote_0(user_id, feed_id)
        vote_mc_flush(user_id, feed_id)

def vote_mc_flush(user_id, feed_id):
    mc_vote_state.delete('%s_%s' % (user_id, feed_id))
    vote_up_count.delete(feed_id)
    vote_down_count.delete(feed_id)
    vote_count.delete(feed_id)
    mc_feed_tuple.delete(feed_id)

if __name__ == '__main__':
    pass
    print vote_count(15)
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
#def rate_up_incr(feed_id):
#    Rate.raw_sql('insert into rate (id, up) values (%s, 1) on duplicate key update up=up+1', feed_id)
#
#def rate_up_decr(feed_id):
#    Rate.raw_sql('update rate set up=up-1 where id=%s', feed_id)
#
#def rate_down_incr(feed_id):
#    Rate.raw_sql('insert into rate (id, down) values (%s, 1) on duplicate key update down=down+1', feed_id)
#
#def rate_down_decr(feed_id):
#    Rate.raw_sql('update rate set down=down-1 where id=%s', feed_id)
#
#def rate_up2down(feed_id):
#    Rate.raw_sql('update rate set up=up-1 and down=down+1 where id=%s', feed_id)
#
#def rate_down2up(feed_id):
#    Rate.raw_sql('update rate set up=up+1 and down=down-1 where id=%s', feed_id)
