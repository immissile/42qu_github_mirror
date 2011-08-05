#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""
1. 通知发起者写总结(是po的文章)
2. 总结写完了以后 , 给所有参与的人重要提醒, 让大家来反馈
6. 如果发起者没有来查看反馈 , 则每日提醒他有哪些人反馈 (重要提醒)

"""
import _env
import time
from model.event import Event, EventUser, CID_EVENT, CID_EVENT_WAIT_SUMMARY, CID_EVENT_WAIT_FEEDBACK 
from model.notice import notice_new
from zweb.orm import ormiter

def event_notice():
    now = int(time.time())
    for event in ormiter(Event, "cid = %s and end_time<%s"%(EVENT_END, now)):
        notice_new(event.id, event.zsite_id, CID_EVENT_WAIT_SUMMARY, 0)
        event.state = CID_EVENT_WAIT_SUMMARY
        event.save()
        
def event_user_notice():
    now = int(time.time())
    for user in ormiter(EventUser, "cid = %s and end_time<%s"(EVENT_USER_END, now)):
        notcie_new(user.event_id, user.user_id, CID_EVENT_WAIT_FEEDBACK, 0)
        event.state = CID_EVENT_USER_WAIT_FEEDBACK
        event.save()

