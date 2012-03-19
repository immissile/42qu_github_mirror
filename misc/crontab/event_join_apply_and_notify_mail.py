#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from model.event import EventJoiner, event_review_join_apply, EVENT_JOIN_STATE_NEW, event_ready, EVENT_STATE_BEGIN, Event, event_pay, EVENT_STATE_END
from time import time, timezone, sleep
from model.kv_misc import kv_int_call, KV_EVENT_READY, KV_EVENT_PAY
from zkit.single_process import single_process
from zweb.orm import ormiter
from model.days import today_days, ONE_DAY_MINUTE
from model.mail import rendermail
from model.mail_notice import mail_notice_state
from model.money import pay_event_get

def buzz_join_apply_review_mail():
    ago = int(time()) - 18*60*60

    c = EventJoiner.raw_sql('select distinct(event_id) from event_joiner where state=%s and create_time<%s;', EVENT_JOIN_STATE_NEW, ago)

    event_id_list = c.fetchall()

    for event_id, in event_id_list:
        event_review_join_apply(event_id)

def event_ready_mail(begin):
    end = (today_days() + 3) * ONE_DAY_MINUTE
    for event in ormiter(Event, 'state=%s and begin_time>%s and begin_time<=%s' % (EVENT_STATE_BEGIN, begin, end)):
        event_ready(event)
    return end

def event_pay_mail(begin):
    end = int(time() - timezone) // 60 - 3 * ONE_DAY_MINUTE
    for i in ormiter(Event, 'state=%s and cent>0 and end_time>%s and end_time<=%s' % (EVENT_STATE_END, begin, end)):
        event_pay(i)
        sleep(0.1)
    return end


@single_process
def main():
    buzz_join_apply_review_mail()
    kv_int_call(KV_EVENT_READY, event_ready_mail)
    kv_int_call(KV_EVENT_PAY, event_pay_mail)

if __name__ == '__main__':
    main()
