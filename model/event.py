#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McCacheA, McLimitA, McNum
from time import time
from zkit.attrcache import attrcache
from money import read_cent, pay_event_get, trade_fail, trade_finish
from zsite import Zsite
from namecard import namecard_bind
from operator import itemgetter
from gid import gid
from po import Po, po_rm, po_state_set
from state import STATE_DEL, STATE_SECRET, STATE_ACTIVE
from mail import rendermail
from zkit.time_format import time_title
from spammer import is_same_post
from po import po_new
from model.cid import CID_EVENT_FEEDBACK
from model.txt import txt_new

mc_event_id_list_by_zsite_id = McLimitA('EventIdListByZsiteId.%s', 128)

event_list_join_by_user_id_query = lambda user_id: EventJoiner.where(
    user_id=user_id
).where('state>=%s' % EVENT_JOIN_STATE_YES)

event_join_count_by_user_id = McNum(
    lambda user_id: event_list_join_by_user_id_query(
        user_id
    ).count(), 'EventJoinCountByUserId.%s'
)

event_joiner_check_query = lambda event_id: EventJoiner.where(event_id=event_id, state=EVENT_JOIN_STATE_NEW)

event_joiner_check_count = McNum(
    lambda event_id: event_joiner_check_query(
        event_id
    ).count(), 'EventJoinerCheckCount.%s'
)

mc_event_id_list_join_by_user_id = McLimitA('EventIdListJoinByUserId.%s', 128)

event_list_open_by_user_id_qs = lambda user_id: EventJoiner.where(user_id=user_id, state=EVENT_JOIN_STATE_YES)
event_open_count_by_user_id = McNum(lambda user_id: event_list_open_by_user_id_qs(user_id).count(), 'EventOpenCountByUserId.%s')

mc_event_id_list_open_by_user_id = McLimitA('EventIdListOpenByUserId.%s', 128)

mc_event_joiner_id_get = McCache('EventJoinerIdGet.%s')

mc_event_joiner_id_list = McCacheA('EventJoinerIdList.%s')
mc_event_joiner_user_id_list = McCacheA('EventJoinerUserIdList.%s')

event_to_review_count_by_zsite_id = McNum(lambda zsite_id: Event.where(state=EVENT_STATE_TO_REVIEW, zsite_id=zsite_id).count(), "EventToReviewCountByZsiteId:%s")

event_count_by_zsite_id = McNum(lambda zsite_id, can_admin: Event.where(zsite_id=zsite_id).where(
    'state between %s and %s',EVENT_STATE_REJECT, EVENT_VIEW_STATE_GET[can_admin]
).count(), 'EventCountByZsiteId.%s')

event_feedback_count = McNum(lambda event_id, state: EventJoiner.where(event_id=event_id, state=state).count(), "EventFeedbackCount:%s")

EVENT_CID_CN = (
    (1 , '技术'),
    (2 , '创业'),
    (3 , '展览'),
    (4 , '电影'),
    (5 , '体育'),
    (6 , '旅行'),
    (7 , '公益'),
    (8 , '讲座'),
    (9 , '曲艺'),
    (10, '聚会'),
    (11, '演出'),
    (12, '其他'),
)
EVENT_CID = tuple(map(itemgetter(0), EVENT_CID_CN))

EVENT_STATE_DEL = 10
EVENT_STATE_INIT = 20
EVENT_STATE_REJECT = 30
EVENT_STATE_TO_REVIEW = 40
EVENT_STATE_BEGIN = 50
EVENT_STATE_NOW = 60
EVENT_STATE_END = 70
EVENT_STATE_SUMMARIZED = 80

EVENT_STATE_CN = {
    EVENT_STATE_DEL:'已删除',
    EVENT_STATE_REJECT: '被拒绝',
    EVENT_STATE_TO_REVIEW: '待审核',
    EVENT_STATE_BEGIN: '未开始',
    EVENT_STATE_NOW: '进行中',
    EVENT_STATE_END: '已结束',
}

EVENT_VIEW_STATE_GET = {
    True: EVENT_STATE_TO_REVIEW,
    False: EVENT_STATE_BEGIN,
}

EVENT_JOIN_STATE_NO = 10
EVENT_JOIN_STATE_NEW = 20
EVENT_JOIN_STATE_YES = 30
EVENT_JOIN_STATE_END = 40
EVENT_JOIN_STATE_REVIEW = 50
EVENT_JOIN_STATE_GENERAL = 60
EVENT_JOIN_STATE_PRAISE = 70 

"""
CREATE TABLE  `zpage`.`event` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `city_pid` int(10) unsigned NOT NULL,
  `pid` int(10) unsigned NOT NULL,
  `address` varchar(255) collate utf8_bin NOT NULL,
  `transport` varchar(255) collate utf8_bin NOT NULL,
  `begin_time` int(10) unsigned NOT NULL default '0',
  `end_time` int(10) unsigned NOT NULL default '0',
  `cent` int(10) unsigned NOT NULL default '0',
  `state` tinyint(3) unsigned NOT NULL,
  `need_review` int(10) unsigned NOT NULL,
  `cid` tinyint(3) unsigned NOT NULL,
  `zsite_id` int(10) unsigned NOT NULL,
  `limit_up` int(10) unsigned NOT NULL default '0',
  `phone` varbinary(64) NOT NULL,
  `limit_down` int(10) unsigned NOT NULL,
  `pic_id` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `Index_3` (`zsite_id`),
  KEY `Index_2` USING BTREE (`state`,`limit_up`),
  KEY `Index_4` (`city_pid`,`state`)
) ENGINE=MyISAM AUTO_INCREMENT=21 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
"""

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
            event.save()
            return event

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


@mc_event_id_list_by_zsite_id('{zsite_id}_{can_admin}')
def event_id_list_by_zsite_id(zsite_id, can_admin, limit, offset):
    return Event.where(zsite_id=zsite_id).where('state between %s and %s',EVENT_STATE_REJECT, EVENT_VIEW_STATE_GET[can_admin]).order_by('id desc').col_list(limit, offset)

def event_list_by_zsite_id(zsite_id, can_admin, limit, offset):
    id_list = event_id_list_by_zsite_id(zsite_id, bool(can_admin), limit, offset)
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



@mc_event_id_list_open_by_user_id('{user_id}')
def event_id_list_open_by_user_id(user_id, limit, offset):
    return event_list_open_by_user_id_qs(user_id).order_by('id desc').col_list(limit, offset, 'event_id')

def event_list_open_by_user_id(user_id, limit, offset):
    id_list = event_id_list_open_by_user_id(user_id, limit, offset)
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
    o = event_joiner_get(event_id, user_id)
    if o:
        return o.state
    return 0

@mc_event_joiner_user_id_list('{event_id}')
def event_joiner_user_id_list(event_id):
    event = Event.mc_get(event_id)
    zsite_id = event.zsite_id
    return EventJoiner.where(event_id=event_id).where('user_id!=%s and state>=%s', zsite_id, EVENT_JOIN_STATE_YES).col_list(col='user_id')



@mc_event_joiner_id_list('{event_id}')
def event_joiner_id_list(event_id):
    event = Event.mc_get(event_id)
    zsite_id = event.zsite_id
    return EventJoiner.where(event_id=event_id).where('user_id!=%s and state>=%s', zsite_id, EVENT_JOIN_STATE_NEW).order_by('id desc').col_list()

def event_joiner_list(event_id, limit, offset):
    id_list = event_joiner_id_list(event_id)[offset: limit+offset]
    li = EventJoiner.mc_get_list(id_list)
    Zsite.mc_bind(li, 'user', 'user_id')
    namecard_bind(li, 'user_id')
    return li

def event_joiner_user_list(event_id, limit=0, offset=0):
    id_list = event_joiner_id_list(event_id)
    if limit:
        id_list = id_list[offset: limit+offset]
    li = EventJoiner.mc_get_list(id_list)
    _li = [i.user_id for i in li]
    return Zsite.mc_get_list(_li)


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
        mc_event_joiner_id_list.delete(event_id)
        mc_event_joiner_user_id_list.delete(event_id)
        if event.zsite_id != user_id:
            event.join_count += 1
            event.save()
    event_joiner_check_count.delete(event_id)
    return o

def event_joiner_no(o):
    event_id = o.event_id
    user_id = o.user_id
    event = o.event
    if o.state == EVENT_JOIN_STATE_NEW:
        if event.cent:
            t = pay_event_get(event, user_id)
            if not t:
                return
            trade_fail(t)
        o.state = EVENT_JOIN_STATE_NO
        o.save()
        mc_event_joiner_id_list.delete(event_id)
        mc_event_joiner_user_id_list.delete(event_id)
        event_joiner_check_count.delete(event_id)

def event_joiner_yes(o):
    event_id = o.event_id
    user_id = o.user_id
    event = o.event
    if o.state == EVENT_JOIN_STATE_NEW:
        if event.cent:
            t = pay_event_get(o.event, user_id)
            if not t:
                return
        o.state = EVENT_JOIN_STATE_YES
        o.save()
        mc_flush_by_user_id(user_id)
        event_joiner_check_count.delete(event_id)

def mc_flush_by_user_id(user_id):
    mc_event_id_list_join_by_user_id.delete(user_id)
    mc_event_id_list_open_by_user_id.delete(user_id)
    event_join_count_by_user_id.delete(user_id)
    event_open_count_by_user_id.delete(user_id)

def event_joiner_end(o):
    event_id = o.event_id
    user_id = o.user_id
    event = o.event
    if o.state == EVENT_JOIN_STATE_YES:
        if event.cent:
            t = pay_event_get(o.event, user_id)
            if not t:
                return
        o.state = EVENT_JOIN_STATE_END
        o.save()
        mc_event_id_list_open_by_user_id.delete(user_id)
        event_open_count_by_user_id.delete(user_id)

def event_join_review(o):
    event_id = o.event_id
    user_id = o.user_id
    event = o.event
    if o.state == EVENT_JOIN_STATE_END:
        if event.cent:
            t = pay_event_get(o.event, user_id)
            if not t:
                return
            trade_finish(t)
        o.state = EVENT_JOIN_STATE_REVIEW
        o.save()

def event_init2to_review(id):
    event = Event.mc_get(id)
    if event and event.state < EVENT_STATE_TO_REVIEW:
        event.state = EVENT_STATE_TO_REVIEW
        event.save()

        zsite_id = event.zsite_id

        mc_event_id_list_by_zsite_id.delete('%s_%s'%(zsite_id, False))

        event_to_review_count_by_zsite_id.delete(zsite_id)

        return True

def event_rm(user_id, id):
    event = Event.mc_get(id)
    if event.can_admin(user_id) and event.can_change():
        event.state = EVENT_STATE_DEL
        event.save()

        mc_flush_by_zsite_id(event.zsite_id)
        event_to_review_count_by_zsite_id.delete(user_id)
        mc_flush_by_user_id(user_id)

def event_review_yes(id):
    event = Event.mc_get(id)
    if event and event.state == EVENT_STATE_TO_REVIEW:
        event.state = EVENT_STATE_BEGIN
        event.save()
        zsite_id = event.zsite_id
        event_joiner_new(id, zsite_id, EVENT_JOIN_STATE_YES)
        po = Po.mc_get(id)
        po_state_set(po, STATE_ACTIVE)
        from notice import notice_event_yes
        notice_event_yes(event.zsite_id, id)

        mc_event_id_list_by_zsite_id.delete('%s_%s'%(zsite_id, False))

        from user_mail import mail_by_user_id
        rendermail(
            '/mail/event/event_review_yes.txt',
            mail_by_user_id(event.zsite_id),
            event.zsite.name,
            link = event.zsite.link,
            title = event.po.name,
        )


def event_review_no(id, txt):
    event = Event.mc_get(id)
    if event and event.state == EVENT_STATE_TO_REVIEW:
        event.state = EVENT_STATE_REJECT
        event.save()
        from top_notice import top_notice_event_no
        top_notice_event_no(event.zsite_id, id, txt)
        from user_mail import mail_by_user_id
        rendermail(
                '/mail/event/event_review_no.txt',
                mail_by_user_id(event.zsite_id),
                event.zsite.name,
                title = event.po.name,
                reason = txt,
                id=id,
                )


def event_begin2now(event):
    if event.state == EVENT_STATE_BEGIN:
        event.state = EVENT_STATE_NOW
        event.save()

def event_feedback_new(user_id, name, txt, rid):
    if not name and not txt:
        return
    name = name or time_title()
    if not is_same_post(user_id, name, txt):
        m = po_new(CID_EVENT_FEEDBACK, user_id, name, STATE_ACTIVE, rid)
        txt_new(m.id, txt)
        m.feed_new()
        return m

from rank import rank_po_id_list
from po_question import answer_id_get

def event_feedback_list(event_id, zsite_id=0, user_id=0):
    ids = rank_po_id_list(event_id, CID_EVENT_FEEDBACK, 'confidence')
    print "ids:",ids

    if zsite_id == user_id:
        zsite_id = 0

    user_ids = filter(bool, (zsite_id, user_id))
    if user_ids:
        _ids = []
        for i in user_ids:
            user_feedback_id = answer_id_get(i, event_id)
            if user_feedback_id:
                _ids.append(user_feedback_id)
                if user_feedback_id in ids:
                    ids.remove(user_feedback_id)
        if _ids:
            _ids.extend(ids)
            ids = _ids

    li = Po.mc_get_list(ids)
    Zsite.mc_bind(li, 'user', 'user_id')
    return li

if __name__ == '__main__':
    po_list = event_feedback_list(10047337, 10016494, 100001637)
    for x in po_list:
        print "po_list", x.id

    print answer_id_get(10016494, 10047337)
    print answer_id_get(10001299, 10047337)
    print answer_id_get(10001637, 10047337)
    pass
    #print 10001299 in event_joiner_user_id_list(10047337)
    #event_review_no(10047323,'yuyuyuyu')
    #print event_to_review_count(10000000)
    #event_joiner_new(event.id, event.zsite_id, EVENT_JOIN_STATE_YES)
    #event = Event.get(10047312)
    #print event.id ,event.zsite_id
    #o = event_joiner_new(event.id, event.zsite_id, EVENT_JOIN_STATE_YES)
    #print o.id

    pass

