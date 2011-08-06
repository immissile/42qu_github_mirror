#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""
1. 通知发起者写总结(是po的文章)
2. 总结写完了以后 , 给所有参与的人重要提醒, 让大家来反馈
6. 如果发起者没有来查看反馈 , 则每日提醒他有哪些人反馈 (重要提醒)

"""
import _env
import time
from model.event import Event, EventUser, CID_EVENT_WAIT_SUMMARY, CID_EVENT_USER_WAIT_FEEDBACK, CID_EVENT_END, CID_EVENT_USER_END, CID_EVENT_SUMMARIZED
from model.notice import notice_new
from zweb.orm import ormiter

def event_notice():
    now = int(time.time())
    for event in ormiter(Event, "state=%s and end_time<%s"%(CID_EVENT_END, now)):
        notice_new(event.zsite_id, event.zsite_id, CID_EVENT_WAIT_SUMMARY, event.id)
        event.state = CID_EVENT_WAIT_SUMMARY
        event.save()
        
def event_user_notice():
    now = int(time.time())
    for user in ormiter(EventUser, "state=%s"%(CID_EVENT_USER_END)):
        event=Event.get(user.event_id)
        if event.state == CID_EVENT_SUMMARIZED:
            notice_new(event.zsite_id, user.user_id, CID_EVENT_USER_WAIT_FEEDBACK, user.event_id)
            user.state = CID_EVENT_USER_WAIT_FEEDBACK
            event.save()
            print user.user_id


if __name__=="__main__":
    event_notice()
    event_user_notice()
