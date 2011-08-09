#!/usr/bin/dev python
# -*- coding: utf-8 -*-
from _handler import LoginBase
from ctrl._urlmap.me import urlmap
from model.po import Po
from model.po_event import po_event_pic_new , EVENT_CID
from zkit.pic import picopen
from zkit.errtip import Errtip
from zkit.jsdict import JsDict
from zkit.earth import pid_city
from model.days import today_ymd_int, ymd2minute, minute2ymd, ONE_DAY_MINUTE
from model.pic import Pic
from model.cid import CID_EVENT
from model.event import event_new, Event, event_feedback_new, EVENT_STATE_SUMMARIZED
from model.po import po_new, STATE_DEL

#MY from model.event import Event, EventUser, event_feedback_new, CID_EVENT_FEEDBACK, CID_EVENT_INTRODUCTION, CID_EVENT_USER_SATISFACTION, CID_EVENT_USER_GENERAL, CID_EVENT_SUMMARIZED
from model import reply
from model.po_pic import pic_list, pic_list_edit, mc_pic_id_list
from model.cid import CID_EVENT_FEEDBACK

@urlmap('/event/feedback/(\d+)')
class EventFeedback(LoginBase):
    def get(self, event_id):
        user_id = self.current_user_id
        self.cid = CID_EVENT_FEEDBACK
        event = Event.get(event_id)
        feedback_po = event.feedback_po()
        if event.zsite_id == user_id and not feedback_po:
            self.render(
                '/ctrl/me/po/po.htm',
                cid = self.cid,
                po=JsDict(),
                pic_list=pic_list_edit(user_id, 0),
            )
        else:
            self.redirect(feedback_po.link)

    def post(self, event_id):
        event = Event.get(event_id)
        current_user = self.current_user
        current_user_id = self.current_user_id
        feedback_po = event.feedback_po()
        if event.zsite_id == current_user_id and not feedback_po:
            name = self.get_argument('name', None)
            txt = self.get_argument('txt', None)
            m = event_feedback_new(event_id, current_user_id, name, txt)
            if m:
                event.state = EVENT_STATE_SUMMARIZED 
                event.save()
                self.redirect(m.link)
        else:
            self.redirect(feedback_po.link)



@urlmap('/po/event')
@urlmap('/po/event/(\d+)')
class Index(LoginBase):
    def post(self, id=0):
        user_id = self.current_user_id
        errtip = Errtip()
        address = self.get_argument('address', None)
        limit_up = self.get_argument('limit_up', "42")
        limit_down = self.get_argument('limit_down', "0")
        transport = self.get_argument('transport', '')
        price = self.get_argument('price','0')
        phone = self.get_argument('phone','')
        pid = self.get_argument('pid','1')
        event_cid = self.get_argument('event_cid', '')
        begin_time = self.get_argument('begin_time','')
        end_time = self.get_argument('end_time','')
        begin_time = self.get_argument('begin_time','')

        begin_time_hour = self.get_argument('begin_time_hour', '0')
        begin_time_minute = self.get_argument('begin_time_minute', '0')
        end_time_hour = self.get_argument('end_time_hour','0')
        end_time_minute = self.get_argument('end_time_minute','0')

        begin_time_hour = int(begin_time_hour)
        begin_time_minute = int(begin_time_minute)

        end_time_hour = int(end_time_hour)
        end_time_minute = int(end_time_minute)

        if begin_time_hour>23 or begin_time_hour<0:
            begin_time_hour = 10

        if end_time_hour>23 or end_time_hour<0:
            end_time_hour = 11

        if begin_time_minute>59 or begin_time_minute<0:
            begin_time_minute = 0

        if end_time_minute>59 or end_time_minute<0:
            end_time_minute = 30

        if begin_time:
            begin_time = int(begin_time)

        if end_time:
            end_time = int(end_time)


        if begin_time > end_time:
            end_time, begin_time = begin_time, end_time

        if begin_time < today_ymd_int():
            errtip.begin_time = "这个时间 , 属于过去"


        begin = ymd2minute(begin_time)+begin_time_hour*60+begin_time_minute
        end = ymd2minute(end_time)+end_time_hour*60+end_time_minute

        if not event_cid.isdigit():
            errtip.event_cid = "请选择类型"
        else:
            event_cid = int(event_cid)
            if event_cid not in EVENT_CID:
                errtip.event_cid = "请选择类型"

        if not pid.isdigit():
            errtip.pid = "请选择地址"
        else:
            pid = int(pid)
            city_pid = pid_city(pid)
            if not city_pid:
                errtip.pid = "请选择地址"

        if price:
            try:
                price = float(price)
            except:
                errtip.price = "请输入有效的金额"
            if price<0:
                errtip.price = "金额必须大于零"
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


        if not address:
            errtip.address = "请输入详细地址"

        if not phone:
            errtip.phone = "请输入联系电话"

        pic_id = None
        files = self.request.files
        if 'pic' in files:
            pic = files['pic'][0]['body']
            pic = picopen(pic)
            if not pic:
                errtip.pic = "图片格式有误"
            else:
                pic_id = po_event_pic_new(user_id, pic)

        if not pic_id:
            pic_id = self.get_argument('pic_id', None)
            if pic_id:
                o = Pic.get(pic_id)
                if not (o and o.user_id == user_id and o.cid == CID_EVENT):
                    pic_id = None

        if not pic_id:
            errtip.pic = "请上传图片"

        if errtip:
            return self.render(
                errtip=errtip,
                address=address,
                pic_id=pic_id,
                limit_up=limit_up,
                limit_down=limit_down,
                transport=transport,
                price=price,
                phone=phone,
                pid=pid,
                event_cid=event_cid,
                begin_time = begin_time,
                end_time = end_time,
                begin_time_hour = begin_time_hour,
                begin_time_minute = begin_time_minute,
                end_time_hour = end_time_hour,
                end_time_minute = end_time_minute,
            )
        else:
            event = event_new(
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
            if not id:
                id = event.id
                po_new(CID_EVENT, user_id, '', STATE_DEL, id=id)
            return self.redirect("/po/edit/%s"%id)

    def get(self, id=0):
        user_id = self.current_user_id
        if id:
            event = Event.mc_get(id)
            if not event or event.zsite_id != self.current_user_id:
                return self.redirect("/po/event")


            return self.render(
                errtip=Errtip(),
                event_id=id,
                address=event.address,
                pic_id=event.pic_id,
                limit_up=event.limit_up,
                limit_down=event.limit_down,
                transport=event.transport,
                price=event.cent/100.0,
                phone=event.phone,
                pid=event.pid,
                event_cid=event.cid,
                begin_time = minute2ymd(event.begin_time),
                end_time = minute2ymd(event.end_time),
                begin_time_hour = (event.begin_time%ONE_DAY_MINUTE)/60,
                begin_time_minute = event.begin_time%60,
                end_time_hour = (event.end_time%ONE_DAY_MINUTE)/60,
                end_time_minute = event.end_time%60,
            )

        return self.render(errtip=Errtip())



