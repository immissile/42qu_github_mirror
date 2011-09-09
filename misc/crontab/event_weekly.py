#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from model.kv_misc import kv_int_call, KV_EVENT_WEEK
from model.cid import CID_USER, CID_MAIL_WEEK
from model.zsite import Zsite, ZSITE_STATE_ACTIVE
from model.mail import rendermail
from model.user_mail import mail_by_user_id
from model.po import Po
from model.event import Event, EVENT_STATE_BEGIN
from model.mail_notice import mail_notice_state
from model.namecard import namecard_get
from model.days import today_cn_date
from zkit.earth import pid_city, PID2NAME, PLACE_MUNI, pid_province, place_name
from zkit.single_process import single_process
from zweb.orm import ormiter
from collections import defaultdict
from zkit.ordereddict import OrderedDict
from zkit.orderedset import OrderedSet
import time
import sys

def event_city_info(event_city_list, pid):
    event_city_list.sort(reverse=True, key=lambda x: city_event_weight(x, pid))
    count = 0
    place = ''
    if pid:
        first = event_city_list[0]
        if first.pid == pid:
            count = len(first.event_list)
            place = PID2NAME[pid]
        else:
            province_id = pid_province(pid)
            #print place_name(province_id)
            li = filter(lambda x: x.province_id == province_id, event_city_list)
            if li:
                count = sum([len(i.event_list) for i in li])
                place = place_name(province_id)

    return event_city_list, count, place


def event_weekly_mail(user, event_city_list):
    user_id = user.id
    if mail_notice_state(user_id, CID_MAIL_WEEK):
        mail = mail_by_user_id(user_id)
        #print user_id
        #sys.stdout.flush()
        if mail:
            title = [
                '线下活动 . 周报汇总'
            ]
            pid = 0
            namecard = namecard_get(user_id)
            if namecard:
                pid_now = namecard.pid_now
                if pid_now:
                    pid = pid_city(pid_now)
            event_city_list, event_incr, place = event_city_info(event_city_list, pid)

            if event_incr:
                title.append(
                    '%s +%s 活动' % (place, event_incr)
                )

            title.append(today_cn_date())
            title = ' . '.join(title)

            name = user.name

            rendermail(
                '/mail/event/weekly.htm',
                mail,
                name,
                event_city_list=event_city_list,
                format='html',
                subject=title
            )


class CityEvent(object):
    def __init__(self, pid, event_list):
        self.pid = pid
        self.place = place_name(pid)
        self.province_id = pid_province(pid)
        event_list.sort(key=lambda x: x.begin_time)
        Po.mc_bind(event_list, 'po', 'id')
        self.event_list = event_list


PID_WEIGHT_DICT = {
    4295032832: 99, # 北京
    4295098368: 98, # 上海
    4529913856: 97, # 广州
}


def city_event_weight(o, pid):
    o_pid = o.pid
    if pid:
        if o_pid == pid:
            return 200
        elif o.province_id == pid_province(pid):
            return 100
    return PID_WEIGHT_DICT.get(o_pid, 0)


def event_city_list(event_list):
    event_dict = defaultdict(list)
    for i in event_list:
        event_dict[i.city_pid].append(i)
    li = []
    for k, v in event_dict.iteritems():
        li.append(CityEvent(k, v))
    return li

def event_weekly(begin):
    event_list = Event.where(state=EVENT_STATE_BEGIN).where('id>%s', begin)
    if event_list:
        last_id = event_list[-1].id
        event_li = event_city_list(event_list)
        for i in ormiter(Zsite, 'cid=%s and state>=%s' % (CID_USER, ZSITE_STATE_ACTIVE)):
            event_weekly_mail(i, event_li)
            #print i.id
            #sys.stdout.flush()
            time.sleep(0.1)
        return last_id

@single_process
def main():
    kv_int_call(KV_EVENT_WEEK, event_weekly)

if __name__ == '__main__':
    main()
