#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McCacheA, McLimitA, McNum, McCacheM
from time import time, sleep
from zkit.attrcache import attrcache
from money import read_cent, pay_event_get, trade_fail, trade_finish
from zsite import Zsite
from namecard import namecard_bind
from career import career_bind
from ico import pic_url_bind_with_default
from operator import itemgetter
from gid import gid
from po import Po, po_rm, po_state_set
from state import STATE_RM, STATE_SECRET, STATE_ACTIVE, STATE_PO_ZSITE_SHOW_THEN_REVIEW
from feed_po import mc_feed_po_dict
from mail import mq_rendermail, rendermail
from notice import notice_event_yes, notice_event_no, notice_event_join_yes, notice_event_join_no
from mq import mq_client
from feed import feed_new, mc_feed_tuple, feed_rm
from user_mail import mail_by_user_id
from days import date_time_by_minute

mc_event_id_list_by_zsite_id = McLimitA('EventIdListByZsiteId.%s', 128)
mc_event_id_list_by_city_pid_cid = McLimitA('EventIdListByCityPidCid.%s', 128)
mc_event_cid_count_by_city_pid = McCacheA('EventCidCountByCityPid.%s')
mc_event_end_id_list_by_city_pid = McLimitA('EventEndIdListByCityPid.%s', 128)
mc_event_all_id_list = McLimitA('EventAllIdList.%s', 128)
event_joiner_new_count = McNum(
    lambda event_id: EventJoiner.where(event_id=event_id, state=EVENT_JOIN_STATE_NEW).count(), 'EventJoinerCheckCount!%s'
)
mc_event_joiner_by_owner_id = McCacheM('EventJoinerByUserId&%s')

event_joiner_feedback_normal_count = McNum( lambda event_id : EventJoiner.where( event_id=event_id, state=EVENT_JOIN_STATE_FEEDBACK_NORMAL).count(), 'EventJoinerFeedbackNormalCount:%s')

event_joiner_feedback_good_count = McNum( lambda event_id : EventJoiner.where( event_id=event_id, state=EVENT_JOIN_STATE_FEEDBACK_GOOD).count(), 'EventJoinerFeedbackGoodCount:%s')


def event_by_city_pid_cid_query(city_pid, cid=0):
    qs = Event.where(city_pid=city_pid)
    if cid:
        qs = qs.where(cid=cid)
    return qs.where('state between %s and %s', EVENT_STATE_BEGIN, EVENT_STATE_NOW)

event_count_by_city_pid_cid = McNum(
    lambda city_pid, cid: event_by_city_pid_cid_query(city_pid, cid).count(),
    'EventCountByCityPidCid.%s'
)

def event_end_by_city_pid_query(city_pid):
    return Event.where(state=EVENT_STATE_END, city_pid=city_pid)

event_end_count_by_city_pid = McNum(
    lambda city_pid: event_end_by_city_pid_query(city_pid).count(),
    'EventEndCountByCityPid.%s'
)

mc_event_joiner_feedback_normal_id_list = McCacheA('EventJoinerReveiwIdList:%s')

event_list_join_by_user_id_query = lambda user_id: EventJoiner.where(
    user_id=user_id
).where('state>=%s' % EVENT_JOIN_STATE_YES)

event_join_count_by_user_id = McNum(
    lambda user_id: event_list_join_by_user_id_query(
        user_id
    ).count(), 'EventJoinCountByUserId.%s'
)


mc_event_id_list_join_by_user_id = McLimitA('EventIdListJoinByUserId.%s', 128)

mc_event_joiner_id_get = McCache('EventJoinerIdGet.%s')

mc_event_joiner_user_id_list = McCacheA('EventJoinerUserIdList.%s')
mc_event_joining_id_list = McCacheA('EventJoiningIdList.%s')
mc_event_joined_id_list = McCacheA('EventJoinedIdList.%s')

event_to_review_count_by_zsite_id = McNum(lambda zsite_id: Event.where(state=EVENT_STATE_TO_REVIEW, zsite_id=zsite_id).count(), 'EventToReviewCountByZsiteId:%s')

event_count_by_zsite_id = McNum(lambda zsite_id, can_admin: Event.where(zsite_id=zsite_id).where(
    'state between %s and %s', EVENT_STATE_REJECT, EVENT_VIEW_STATE_GET[can_admin]
).count(), 'EventCountByZsiteId.%s')


EVENT_CID_CN = (
    (1 , '讲座'),
    (2 , '电影'),
    (3 , '展览'),
    (4 , '体育'),
    (5 , '旅行'),
    (6 , '公益'),
    (7 , '聚会'),
    (8 , '演出'),
    (9 , '其他'),
)

EVENT_CID = tuple(map(itemgetter(0), EVENT_CID_CN))

EVENT_STATE_RM = 10
EVENT_STATE_INIT = 20
EVENT_STATE_REJECT = 30
EVENT_STATE_TO_REVIEW = 40
EVENT_STATE_BEGIN = 50
EVENT_STATE_NOW = 60
EVENT_STATE_END = 70

EVENT_STATE_CN_TUPLE = (
    (EVENT_STATE_RM, '已删除'),
    (EVENT_STATE_REJECT, '被拒绝'),
    (EVENT_STATE_TO_REVIEW, '待审核'),
    (EVENT_STATE_BEGIN, '未开始'),
    (EVENT_STATE_NOW, '进行中'),
    (EVENT_STATE_END, '已结束'),
)
EVENT_STATE_CN = dict(EVENT_STATE_CN_TUPLE)

EVENT_VIEW_STATE_GET = {
    True: EVENT_STATE_TO_REVIEW,
    False: EVENT_STATE_BEGIN,
}

EVENT_JOIN_STATE_NO = 10
EVENT_JOIN_STATE_NEW = 20
EVENT_JOIN_STATE_YES = 30
EVENT_JOIN_STATE_END = 40
EVENT_JOIN_STATE_FEEDBACK_NORMAL = 50
EVENT_JOIN_STATE_FEEDBACK_GOOD = 60


def event_new_if_can_change(
    zsite_id,
    cid,
    city_pid,
    pid,
    address,
    transport,
    begin_time,
    end_time,
    cent,
    limit_up,
    limit_down,
    phone,
    pic_id,
    id=None
):
    if id:
        event = Event.mc_get(id)
        if event and not event.can_change():
            event.phone = phone
            event.pic_id = pic_id
            event.limit_up = limit_up
            event.limit_down = limit_down
            event.save()
            return event
        mc_feed_po_dict.delete(id)

    return event_new(
        zsite_id,
        cid,
        city_pid,
        pid,
        address,
        transport,
        begin_time,
        end_time,
        cent,
        limit_up,
        limit_down,
        phone,
        pic_id,
        id=id
    )


def event_new(
    zsite_id,
    cid,
    city_pid,
    pid,
    address,
    transport,
    begin_time,
    end_time,
    cent,
    limit_up,
    limit_down,
    phone,
    pic_id,
    id=None
):
    if id:
        event = Event.mc_get(id)
        if event.zsite_id == zsite_id:
            event.cid = cid
            event.city_pid = city_pid
            event.pid = pid
            event.address = address
            event.transport = transport
            event.begin_time = begin_time
            event.end_time = end_time
            event.cent = cent
            event.limit_up = limit_up
            event.limit_down = limit_down
            event.phone = phone
            event.pic_id = pic_id
            #event.state=EVENT_STATE_INIT
            event.save()
    else:
        event = Event(
            id=gid(),
            zsite_id=zsite_id,
            cid=cid,
            city_pid=city_pid,
            pid=pid,
            address=address,
            transport=transport,
            begin_time=begin_time,
            end_time=end_time,
            cent=cent,
            limit_up=limit_up,
            limit_down=limit_down,
            phone=phone,
            pic_id=pic_id,
            state=EVENT_STATE_INIT
        )
        event.save()
        mc_flush_by_zsite_id(zsite_id)

    return event


def mc_flush_by_zsite_id(zsite_id):
    for i in (True, False):
        mc_key = '%s_%s' % (zsite_id, i)
        mc_event_id_list_by_zsite_id.delete(mc_key)
        event_count_by_zsite_id.delete(mc_key)


class Event(McModel):
    def can_admin(self, user_id):
        if self.zsite_id == user_id:
            return True

    def can_change(self):
        if self.join_count == 0:
            return True
        if self.state <= EVENT_STATE_TO_REVIEW:
            return True

    @attrcache
    def price(self):
        cent = self.cent
        if cent:
            return read_cent(cent)
        return ''

    @attrcache
    def zsite(self):
        return Zsite.mc_get(self.zsite_id)

    @attrcache
    def po(self):
        return Po.mc_get(self.id)

    @attrcache
    def link(self):
        o = self.zsite
        return '%s/%s' % (o.link, self.id)


@mc_event_all_id_list('')
def event_all_id_list(limit, offset):
    return Event.where('state>=%s', EVENT_STATE_BEGIN).order_by('id desc').col_list(limit, offset)

def event_all_list(limit, offset):
    id_list = event_all_id_list(limit, offset)
    return zip(Event.mc_get_list(id_list), Po.mc_get_list(id_list))


@mc_event_id_list_by_zsite_id('{zsite_id}_{can_admin}')
def event_id_list_by_zsite_id(zsite_id, can_admin, limit, offset):
    return Event.where(zsite_id=zsite_id).where('state between %s and %s', EVENT_STATE_REJECT, EVENT_VIEW_STATE_GET[can_admin]).order_by('id desc').col_list(limit, offset)

def event_list_by_zsite_id(zsite_id, can_admin, limit, offset):
    id_list = event_id_list_by_zsite_id(zsite_id, bool(can_admin), limit, offset)
    return zip(Event.mc_get_list(id_list), Po.mc_get_list(id_list))

def last_event_by_zsite_id(zsite_id):
    event = Event.where(zsite_id=zsite_id).order_by('id desc')[0]
    return event


@mc_event_id_list_by_city_pid_cid('{city_pid}_{cid}')
def event_id_list_by_city_pid_cid(city_pid, cid, limit=10, offset=0):
    return event_by_city_pid_cid_query(city_pid, cid).order_by('end_time').col_list(limit, offset)

def event_list_by_city_pid_cid(city_pid, cid, limit=10, offset=0):
    id_list = event_id_list_by_city_pid_cid(city_pid, cid, limit, offset)
    return zip(Event.mc_get_list(id_list), Po.mc_get_list(id_list))


@mc_event_end_id_list_by_city_pid('{city_pid}')
def event_end_id_list_by_city_pid(city_pid, limit, offset):
    return event_end_by_city_pid_query(city_pid).order_by('end_time desc').col_list(limit, offset)

def event_end_list_by_city_pid(city_pid, limit, offset):
    id_list = event_end_id_list_by_city_pid(city_pid, limit, offset)
    return zip(Event.mc_get_list(id_list), Po.mc_get_list(id_list))


class EventJoiner(McModel):
    @attrcache
    def event(self):
        return Event.mc_get(self.event_id)


@mc_event_id_list_join_by_user_id('{user_id}')
def event_id_list_join_by_user_id(user_id, limit, offset):
    return event_list_join_by_user_id_query(user_id).order_by('id desc').col_list(limit, offset, 'event_id')

def event_list_join_by_user_id(user_id, limit, offset):
    id_list = event_id_list_join_by_user_id(user_id, limit, offset)
    return zip(Event.mc_get_list(id_list), Po.mc_get_list(id_list))


@mc_event_joiner_id_get('{event_id}_{user_id}')
def event_joiner_id_get(event_id, user_id):
    o = EventJoiner.get(event_id=event_id, user_id=user_id)
    if o:
        return o.id
    return 0

def event_joiner_get(event_id, user_id):
    id = event_joiner_id_get(event_id, user_id)
    if id:
        return EventJoiner.mc_get(id)

def event_joiner_state(event_id, user_id):
    if user_id:
        o = event_joiner_get(event_id, user_id)
        if o:
            return o.state
    return 0


@mc_event_joiner_feedback_normal_id_list('{event_id}')
def event_joiner_feedback_normal_id_list(event_id):
    return EventJoiner.where(
        event_id=event_id, state=EVENT_JOIN_STATE_FEEDBACK_NORMAL
    ).col_list(col='user_id')




def mc_flush_feedback(event_id):
    mc_event_joiner_feedback_normal_id_list.delete(event_id)
    event_joiner_feedback_normal_count.delete(event_id)
    event_joiner_feedback_good_count.delete(event_id)


@mc_event_joining_id_list('{event_id}')
def event_joining_id_list(event_id):
    return EventJoiner.where(event_id=event_id, state=EVENT_JOIN_STATE_NEW).order_by('id desc').col_list()

@mc_event_joined_id_list('{event_id}')
def event_joined_id_list(event_id):
    event = Event.mc_get(event_id)
    zsite_id = event.zsite_id
    return EventJoiner.where(event_id=event_id).where('user_id!=%s and state>=%s', zsite_id, EVENT_JOIN_STATE_YES).order_by('id desc').col_list()

def event_joiner_id_list(event_id, limit, offset):
    li = []
    li.extend(event_joining_id_list(event_id))
    li.extend(event_joined_id_list(event_id))
    return li[offset: offset+limit]

def event_joiner_split_before_id(li):
    if li:
        first = li[0].id
        for i in li:
            if i.state == EVENT_JOIN_STATE_YES:
                id = i.id
                if id == first:
                    return 0
                return id
    return 0

def event_joiner_list(event_id, limit, offset):
    id_list = event_joiner_id_list(event_id, limit, offset)
    li = EventJoiner.mc_get_list(id_list)
    split_before_id = event_joiner_split_before_id(li)
    Zsite.mc_bind(li, 'user', 'user_id')
    user_list = [i.user for i in li]
    namecard_bind(user_list)
    career_bind(user_list)
    pic_url_bind_with_default(user_list, '96')
    return li, split_before_id

@mc_event_joiner_user_id_list('{event_id}')
def event_joiner_user_id_list(event_id):
    event = Event.mc_get(event_id)
    if event:
        zsite_id = event.zsite_id
        return EventJoiner.where(event_id=event_id).where('user_id!=%s and state>=%s', zsite_id, EVENT_JOIN_STATE_NEW).order_by('id desc').col_list(col='user_id')
    return []

def event_joiner_user_list(event_id, limit=0, offset=0):
    id_list = event_joiner_user_id_list(event_id)
    if limit:
        id_list = id_list[offset: limit+offset]
    return Zsite.mc_get_list(id_list)


def event_joiner_new(event_id, user_id, state=EVENT_JOIN_STATE_NEW):
    event = Event.mc_get(event_id)
    if not event or \
        event.state < EVENT_STATE_BEGIN or \
        event.state >= EVENT_STATE_END:
        return

    o = event_joiner_get(event_id, user_id)
    if o and o.state >= state:
        return o

    now = int(time())

    if o:
        o.state = state
        o.create_time = now
        o.save()
    else:
        o = EventJoiner.get_or_create(event_id=event_id, user_id=user_id)
        o.state = state
        o.create_time = now
        o.save()
        mc_event_joiner_id_get.set('%s_%s' % (event_id, user_id), o.id)



    if event.zsite_id != user_id:
        event.join_count += 1
        event.save()

    mc_flush_by_user_id_event_id_owner_id(user_id, event_id, event.zsite_id)
    return o


def event_joiner_can_exit(event_id, user_id):
    if event_joiner_state(event_id, user_id) in (EVENT_JOIN_STATE_NEW, EVENT_JOIN_STATE_YES):
        event = Event.mc_get(event_id)
        if event.cent:
            if pay_event_get(event, user_id):
                return False
        return True


def event_joiner_exit(event_id, user_id):
    if event_joiner_can_exit(event_id, user_id):
        o = event_joiner_get(event_id, user_id)
        event_joiner_no(o)


def event_joiner_no(o, txt=''):
    event_id = o.event_id
    user_id = o.user_id
    event = o.event
    zsite_id = event.zsite_id
    if o.state in (EVENT_JOIN_STATE_NEW, EVENT_JOIN_STATE_YES):
        if event.cent:
            t = pay_event_get(event, user_id)
            if t:
                trade_fail(t)
        o.state = EVENT_JOIN_STATE_NO
        o.save()
        if zsite_id != user_id:
            event.join_count -= 1
            event.save()
        if txt:
            notice_event_join_no(zsite_id, user_id, event_id, txt)
        mc_flush_by_user_id_event_id_owner_id(user_id, event_id, zsite_id)

def event_joiner_yes(o):
    event_id = o.event_id
    user_id = o.user_id
    event = o.event
    zsite_id = event.zsite_id
    if o.state == EVENT_JOIN_STATE_NEW:
        o.state = EVENT_JOIN_STATE_YES
        o.save()
        notice_event_join_yes(zsite_id, user_id, event_id)
        from model.buzz import mq_buzz_event_join_new
        mq_buzz_event_join_new(user_id, event_id, zsite_id)
        mc_flush_by_user_id_event_id_owner_id(user_id, event_id, event.zsite_id)

def event_ready(event):
    join_count = event.join_count
    po = event.po
    link = 'http:%s' % po.link
    title = po.name
    begin_time = date_time_by_minute(event.begin_time)
    user_id_list = event_joiner_user_id_list(event.id)
    user_id_list.append(event.zsite_id)
    for user_id in user_id_list:
        rendermail(
            '/mail/event/event_ready.txt',
            mail_by_user_id(user_id),
            Zsite.mc_get(user_id).name,
            link=link,
            title=title,
            begin_time=begin_time,
            join_count=join_count,
        )
        sleep(0.1)


def mc_flush_by_user_id_event_id_owner_id(user_id, event_id, owner_id):
    if user_id:
        mc_event_id_list_join_by_user_id.delete(user_id)
        event_join_count_by_user_id.delete(user_id)

    mc_event_joiner_user_id_list.delete(event_id)
    mc_event_joining_id_list.delete(event_id)
    mc_event_joined_id_list.delete(event_id)
    event_joiner_new_count.delete(event_id)

    mc_event_joiner_by_owner_id.delete(owner_id)

def mc_flush_by_city_pid_cid(city_pid, cid):
    for _cid in set([0, cid]):
        mc_event_id_list_by_city_pid_cid.delete('%s_%s'%(city_pid, _cid))
        event_count_by_city_pid_cid.delete(city_pid, _cid)
    mc_event_cid_count_by_city_pid.delete(city_pid)
    mc_event_end_id_list_by_city_pid.delete(city_pid)
    event_end_count_by_city_pid.delete(city_pid)
    mc_event_all_id_list.delete('')


def event_init2to_review(id):
    event = Event.mc_get(id)
    if event and event.state <= EVENT_STATE_TO_REVIEW:
        if event.state < EVENT_STATE_TO_REVIEW:

            event.state = EVENT_STATE_TO_REVIEW
            event.save()

            zsite_id = event.zsite_id

            mc_event_id_list_by_zsite_id.delete('%s_%s'%(zsite_id, False))

            event_to_review_count_by_zsite_id.delete(zsite_id)

            return True
        return True


def event_kill_extra(from_id, event_id, po_id):
    from notice import notice_event_kill_one, notice_event_kill_mail
    event_po = Po.mc_get(event_id)
    title = event_po.name
    event = Event.mc_get(event_id)
    link = event.link
    po = Po.mc_get(event_id)
    txt = po.name
    notice_link = po.link
    for i in EventJoiner.where(event_id=event_id).where('state>=%s', EVENT_JOIN_STATE_NEW):
        event_joiner_no(i)
        user_id = i.user_id
        notice_event_kill_one(from_id, user_id, po_id)
        notice_event_kill_mail(user_id, title, link, txt, notice_link)

mq_event_kill_extra = mq_client(event_kill_extra)

def event_kill(user_id, event, txt):
    from po_event import _po_event_notice_new
    if EVENT_STATE_RM < event.state < EVENT_STATE_END:
        event_id = event.id
        if event.can_change():
            po_rm(user_id, event_id)
        else:
            event.state = EVENT_STATE_RM
            event.save()
            zsite_id = event.zsite_id
            feed_rm(event_id)
            mc_flush_by_zsite_id(zsite_id)
            event_to_review_count_by_zsite_id.delete(user_id)
            mc_flush_by_user_id_event_id_owner_id(user_id, id, zsite_id)

        o = _po_event_notice_new(user_id, event_id, txt)
        mq_event_kill_extra(user_id, event_id, o.id)
        mc_flush_by_city_pid_cid(event.city_pid, event.cid)


def event_rm(user_id, id):
    event = Event.mc_get(id)
    if event and event.can_change():
        event.state = EVENT_STATE_RM
        event.save()
        zsite_id = event.zsite_id
        mc_flush_by_zsite_id(event.zsite_id)
        event_to_review_count_by_zsite_id.delete(user_id)
        mc_flush_by_user_id_event_id_owner_id(user_id, id, zsite_id)


def event_review_yes(id):
    event = Event.mc_get(id)
    #print event,id, event.state

    if event and event.state <= EVENT_STATE_TO_REVIEW:
        event.state = EVENT_STATE_BEGIN
        event.save()
        mc_flush_by_city_pid_cid(event.city_pid, event.cid)

        zsite_id = event.zsite_id
        event_joiner_new(id, zsite_id, EVENT_JOIN_STATE_YES)
        po = Po.mc_get(id)

        if po.zsite_id:
            state = STATE_PO_ZSITE_SHOW_THEN_REVIEW
        else:
            state = STATE_ACTIVE

        po_state_set(po, state)

        notice_event_yes(event.zsite_id, id)

        mc_event_id_list_by_zsite_id.delete('%s_%s'%(zsite_id, False))

        mq_rendermail(
            '/mail/event/event_review_yes.txt',
            mail_by_user_id(event.zsite_id),
            event.zsite.name,
            link=po.link,
            title=po.name,
            price=event.price
        )


def event_review_no(id, txt):
    event = Event.mc_get(id)
    if event and event.state == EVENT_STATE_TO_REVIEW:
        event.state = EVENT_STATE_REJECT
        event.save()
        notice_event_no(event.zsite_id, id, txt)
        zsite = event.zsite
        mq_rendermail(
            '/mail/event/event_review_no.txt',
            mail_by_user_id(event.zsite_id),
            event.zsite.name,
            title=event.po.name,
            reason=txt,
            zsite_link='http:%s'%zsite.link,
            id=id,
        )


def event_begin2now(event):
    if event.state < EVENT_STATE_NOW:
        event.state = EVENT_STATE_NOW
        event.save()
        mc_flush_by_city_pid_cid(event.city_pid, event.cid)


def event_end(event):
    if event.state < EVENT_STATE_END:
        event.state = EVENT_STATE_END
        event.save()
        mc_flush_by_city_pid_cid(event.city_pid, event.cid)
        event_end_mail(event)
        for i in EventJoiner.where(event_id=event.id).where('state in (%s, %s)', EVENT_JOIN_STATE_NEW, EVENT_JOIN_STATE_YES):
            i.state = EVENT_JOIN_STATE_END
            i.save()


def event_pay(event):
    owner = event.zsite
    owner_id = event.zsite_id
    cent = event.cent
    if event.state == EVENT_STATE_END and cent:
        pay_count = 0
        for i in EventJoiner.where(event_id=event.id).where('state>=%s', EVENT_JOIN_STATE_YES):
            user_id = i.user_id
            if user_id != owner_id:
                t = pay_event_get(event, user_id)
                if t:
                    trade_finish(t)
                    pay_count += 1
        if pay_count:
            pay_money = read_cent(cent * pay_count)
            po = event.po
            rendermail(
                '/mail/event/event_end_draw.txt',
                mail_by_user_id(owner_id),
                owner.name,
                join_count=event.join_count,
                pay_count=pay_count,
                pay_money=pay_money,
                title=po.name,
                link=po.link,
            )


def event_end_mail(event):
    event_id = event.id
    owner_id = event.zsite_id
    owner = event.zsite
    po = Po.mc_get(event_id)
    rendermail(
        '/mail/event/event_end_owner.txt',
        mail_by_user_id(owner_id),
        owner.name,
        title=po.name,
        link=po.link,
        user_link=owner.link,
        price=event.price,
        feedback_link='/event/feedback/%s' % event_id
    )
    sleep(0.1)

    for user_id in event_joiner_user_id_list(event_id):
        if user_id != owner_id:
            user = Zsite.mc_get(user_id)
            rendermail(
                '/mail/event/event_end_joiner.txt',
                mail_by_user_id(user_id),
                user.name,
                title=po.name,
                link=po.link,
                user_link=user.link,
                feedback_link='/event/feedback/%s' % event_id
            )
            sleep(0.1)


def event_review_join_apply(event_id):
    event = Event.mc_get(event_id)
    if event:
        event_new_joiner_id_list = EventJoiner.where(
            'event_id=%s and state=%s', event_id, EVENT_JOIN_STATE_NEW
        ).col_list(col='user_id')

        if event_new_joiner_id_list:
            event_joiner_list = [
                user.name
                for user in
                Zsite.mc_get_list(event_new_joiner_id_list)
            ]

            rendermail(
                '/mail/event/event_review_join_apply.txt',
                mail_by_user_id(event.zsite_id),
                event.zsite.name,
                event_link='http:%s/event/check/%s' % (
                    event.zsite.link, event_id
                ),
                title=event.po.name,
                event_join_apply_list=' , '.join(event_joiner_list)
            )
            sleep(0.1)

@mc_event_cid_count_by_city_pid('{city_pid}')
def event_cid_count_by_city_pid(city_pid):
    return [event_count_by_city_pid_cid(city_pid, cid) for cid in EVENT_CID]

def event_cid_name_count_by_city_pid(city_pid):
    for (event_cid, event_cid_name), count in zip(EVENT_CID_CN, event_cid_count_by_city_pid(city_pid)):
        yield event_cid, event_cid_name, count

@mc_event_joiner_by_owner_id('{user_id}')
def event_joiner_by_owner_id(user_id):
    event_id_list = event_id_list_by_zsite_id(user_id, False, None, None)
    result = []
    if event_id_list:
        event_id_list_with_count = []
        event_id_count_list = []
        for id, count in zip(
            event_id_list,
            event_joiner_new_count.get_list(event_id_list)
        ):
            if count:
                event_id_list_with_count.append(id)
                event_id_count_list.append(count)

        for po, count in zip(
            Po.mc_get_list(event_id_list_with_count),
            event_id_count_list
        ):
            result.append((po.id, po.name, count))
    return result

if __name__ == '__main__':
    pass
    #from model.user_mail import mail_by_user_id
    class Vps(Model):
        pass
    #id = 0
    #for i in event_joiner_user_id_list(10236239):
    #    id+=1
    #    if id in (12,):
    #        continue
    #    Vps(state=10,group=1,id_in_group=id, user_id=i).save()
    #    print id, mail_by_user_id(i)
    #from os import urandom
    #from base64 import b64encode
    #print 
    from uuid import uuid4
    for i in Vps.where():
        i.passwd = uuid4().hex[:8].replace("l","k")
        i.save()
    #id = 10242980 
    #event = Event.mc_get(id)
    #event.state = EVENT_STATE_REJECT
    #event.save()

#    for i in Event.where(state=EVENT_STATE_TO_REVIEW):
#        print i.id
#        i.state = EVENT_STATE_REJECT
#        i.save()

    #print event_review_yes(10202687)
#    print last_event_by_zsite_id(10001299).id
#    from zsite import Zsite
#    from po import Po
#    from user_mail import mail_by_user_id
#    for i in Zsite.mc_get_list(set(Event.where('state>=%s', EVENT_STATE_BEGIN).order_by('id desc').col_list(col='zsite_id'))):
#        e = Event.where(zsite_id=i.id)[0]
#        print 'http:%s'%i.link, '---', mail_by_user_id(i.id), '---', 'http:%s'%e.link, '---', Po.mc_get(e.id).name_
#print last_event_by_zsite_id(10001299).id

    #for id , name, j in event_joiner_by_owner_id(10000000):
    #    print id, name, j

    #print event_joiner_new_count(2803)
