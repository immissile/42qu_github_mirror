#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McCacheA, McLimitA, McNum, McCacheM
from po import po_new
from state import STATE_ACTIVE
from txt import txt_new 

CID_EVENT_INTRODUCTION = 69
CID_EVENT_FEEDBACK = 70

CID_EVENT_EDIT = 90
CID_EVENT_REVIEW_FAIL = 91
CID_EVENT_REVIEW = 92
CID_EVENT_REGISTRATION = 94
CID_EVENT_END = 99
CID_EVENT_WAIT_SUMMARY = 100
CID_EVENT_SUMMARIZED = 102

CID_EVENT_USER_INIT = 40
CID_EVENT_USER_PAID = 42
CID_EVENT_USER_QUIT = 44
CID_EVENT_USER_END = 50
CID_EVENT_USER_WAIT_FEEDBACK = 51
CID_EVENT_USER_GENERAL = 52
CID_EVENT_USER_SATISFACTION = 54

class Event(Model):
    pass

class EventUser(Model):
    pass


def test_event_init():
    o = Event()
    o.city_pid = 497866752
    o.pid = 446028032
    o.address = "回龙观 龙锦五区"
    o.transport = "回龙观城铁站下，然后做602路公交车"
    o.begin_time = 1310774406
    o.end_time = 1314230406
    o.price = 0
    o.pay_online = 0
    o.state = CID_EVENT_END
    o.need_review = 0
    o.cid = CID_EVENT_FEEDBACK
    o.zsite_id = 10016494
    o.save()
    return o.id


def test_add_event_user(event_id):
    o = EventUser()
    o.event_id = event_id
    o.user_id = 10016149
    o.create_time = 1312416006
    o.state = CID_EVENT_USER_END
    o.save()
    print "event_user_id:",o.id

    o = EventUser()
    o.event_id = event_id
    o.user_id = 10001518
    o.create_time = 1312414006
    o.state = CID_EVENT_USER_END
    o.save()
    print "event_user_id:",o.id

    o = EventUser()
    o.event_id = event_id
    o.user_id = 10030280
    o.create_time = 1312412006
    o.state = CID_EVENT_USER_END
    o.save()
    print "event_user_id:",o.id


def event_feedback_new(event_id, user_id, name, txt):
    m = po_new(CID_EVENT_FEEDBACK, user_id, name, STATE_ACTIVE, event_id)
    txt_new(m.id, txt)
    return m

def event_feedback_list(po, user_id):
    event_id = po.rid
    event_user_list = EventUser.where("event_id = %s",event_id).col_list(col='user_id')
    can_feedback = not user_id in event_user_list

    return can_feedback, reply_list
if __name__=="__main__":
    #event_id = test_event_init()
    #test_add_event_user(event_id)

