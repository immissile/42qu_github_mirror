#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.user_mail import mail_by_user_id
from model.mail import sendmail
from model.event import Event, event_review_yes, event_review_no, EVENT_STATE_TO_REVIEW
from model.po import Po
from zkit.page import page_limit_offset
from model.days import today_ymd_int, ymd2minute, minute2ymd, ONE_DAY_MINUTE


PAGE_LIMIT = 50

@urlmap('/event/review')
class EventReview(Base):
    def get(self):
        qs = Event.where(state=EVENT_STATE_TO_REVIEW).order_by('id')[:1]
        o = None
        if qs:
            o = qs[0]
        self.render(event=o)


@urlmap('/event')
@urlmap('/event-(\d+)')
class EventIndex(Base):
    def get(self, n=1):
        qs = Event.where()
        total = qs.count()
        page, limit, offset = page_limit_offset(
            '/event-%s',
            total,
            n,
            PAGE_LIMIT,
        )
        li = qs.order_by('id desc')[offset: offset + limit]
        Po.mc_bind(li, 'po', 'id')
        self.render(
            'god/event/event_page.htm',
            stat=0,
            li=li,
            page=page,
        )


@urlmap('/event/(\d+)')
@urlmap('/event/(\d+)-(\d+)')
class EventPage(Base):
    def get(self, state, n=1):
        state = int(state)
        qs = Event.where(state=state)
        total = qs.count()
        page, limit, offset = page_limit_offset(
            '/event/%s-%%s' % state,
            total,
            n,
            PAGE_LIMIT,
        )
        li = qs.order_by('id desc')[offset: offset + limit]
        Po.mc_bind(li, 'po', 'id')
        self.render(
            stat=state,
            li=li,
            page=page,
        )


@urlmap('/event/edit/(\d+)')
class EventEdit(Base):
    def get(self, id):
        event = Event.mc_get(id)
        if event:
            return self.render(
                event_id=id,
                event=event,
                state=event.state,
                address=event.address,
                pic_id=event.pic_id,
                limit_up=event.limit_up,
                limit_down=event.limit_down,
                transport=event.transport,
                price=event.price,
                phone=event.phone,
                pid=event.pid,
                event_cid=event.cid,
                begin_time=minute2ymd(event.begin_time),
                end_time=minute2ymd(event.end_time),
                begin_time_hour=(event.begin_time%ONE_DAY_MINUTE)/60,
                begin_time_minute=event.begin_time%60,
                end_time_hour=(event.end_time%ONE_DAY_MINUTE)/60,
                end_time_minute=event.end_time%60,
            )

    def post(self, id):
        phone = self.get_argument('phone', '')
        address = self.get_argument('address', None)
        limit_up = self.get_argument('limit_up', '42')
        limit_down = self.get_argument('limit_down', '0')
        transport = self.get_argument('transport', '')
        price = self.get_argument('price', '0')
        pid = self.get_argument('pid', '1')
        event_cid = self.get_argument('event_cid', '')
        begin_time = self.get_argument('begin_time', '')
        end_time = self.get_argument('end_time', '')
        begin_time = self.get_argument('begin_time', '')

        begin_time_hour = self.get_argument('begin_time_hour', '0')
        begin_time_minute = self.get_argument('begin_time_minute', '0')
        end_time_hour = self.get_argument('end_time_hour', '0')
        end_time_minute = self.get_argument('end_time_minute', '0')

        begin_time_hour = int(begin_time_hour)
        begin_time_minute = int(begin_time_minute)

        end_time_hour = int(end_time_hour)
        end_time_minute = int(end_time_minute)

        if begin_time_hour > 23 or begin_time_hour < 0:
            begin_time_hour = 10

        if end_time_hour > 23 or end_time_hour < 0:
            end_time_hour = 11

        if begin_time_minute > 59 or begin_time_minute < 0:
            begin_time_minute = 0

        if end_time_minute > 59 or end_time_minute < 0:
            end_time_minute = 30

        if begin_time:
            begin_time = int(begin_time)

        if end_time:
            end_time = int(end_time)


        if begin_time > end_time:
            end_time, begin_time = begin_time, end_time

        if begin_time < today_ymd_int():
            errtip.begin_time = '这个时间 , 属于过去'


        begin = ymd2minute(begin_time)+begin_time_hour*60+begin_time_minute
        end = ymd2minute(end_time)+end_time_hour*60+end_time_minute

        if not event_cid.isdigit():
            errtip.event_cid = '请选择类型'
        else:
            event_cid = int(event_cid)
            if event_cid not in EVENT_CID:
                errtip.event_cid = '请选择类型'

        if not pid.isdigit():
            errtip.pid = '请选择地址'
        else:
            pid = int(pid)
            city_pid = pid_city(pid)
            if not city_pid:
                errtip.pid = '请选择地址'

        if price:
            try:
                price = float(price)
            except:
                errtip.price = '请输入有效的金额'
            if price < 0:
                errtip.price = '金额必须大于零'
        else:
            price = 0

        if not limit_down.isdigit():
            limit_down = 0
        else:
            limit_down = int(limit_down)

        if not limit_up.isdigit():
            limit_up = 42
        else:
            limit_up = int(limit_up)

        if limit_down > limit_up:
            limit_up, limit_down = limit_down, limit_up
        if limit_down < 0:
            errtip.limit_down = "人数不能为负数"

        if not address:
            errtip.address = '请输入详细地址'

        if not phone:
            errtip.phone = '请输入联系电话'

        pic_id = None
        files = self.request.files
        if 'pic' in files:
            pic = files['pic'][0]['body']
            pic = picopen(pic)
            if not pic:
                errtip.pic = '图片格式有误'
            else:
                pic_id = po_event_pic_new(user_id, pic)

        if not pic_id:
            pic_id = self.get_argument('pic_id', None)
            if pic_id:
                o = Pic.get(pic_id)
                if not (o and o.user_id == user_id and o.cid == CID_EVENT):
                    pic_id = None

            event = event_new_if_can_change(
                user_id,
                event_cid,
                city_pid,
                pid,
                address,
                transport,
                begin,
                end,
                int(100*price),
                limit_up,
                limit_down,
                phone,
                pic_id,
                id
            )

        return self.redirect('/%s'%id)


@urlmap('/event/state/(\d+)/(0|1)')
class EventState(Base):
    def post(self, id, state):
        state = int(state)
        if state:
            event_review_yes(id)
        else:
            txt = self.get_argument('txt')
            event_review_no(id, txt)
        self.finish('{}')
