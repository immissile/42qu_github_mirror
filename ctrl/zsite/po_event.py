# -*- coding: utf-8 -*-
from _handler import ZsiteBase, LoginBase, login
from model.zsite_site import zsite_id_by_zsite_user_id
from ctrl._urlmap.zsite import urlmap
from model.po_event import po_event_pic_new , EVENT_CID, po_event_feedback_new
from zkit.pic import picopen
from zkit.errtip import Errtip
from zkit.jsdict import JsDict
from zkit.earth import pid_city
from model.days import today_ymd_int, ymd2minute, minute2ymd, ONE_DAY_MINUTE
from model.pic import Pic
from model.cid import CID_EVENT, CID_EVENT_FEEDBACK, CID_NOTICE_EVENT_JOINER_FEEDBACK, CID_NOTICE_EVENT_ORGANIZER_SUMMARY
from model.state import STATE_RM, STATE_SECRET, STATE_ACTIVE
from model.event import Event, EVENT_STATE_INIT, EVENT_STATE_REJECT, EVENT_STATE_TO_REVIEW, EVENT_STATE_NOW, EVENT_JOIN_STATE_END, EVENT_JOIN_STATE_YES, EVENT_JOIN_STATE_FEEDBACK_GOOD, EVENT_JOIN_STATE_FEEDBACK_NORMAL, event_new_if_can_change, EventJoiner, event_joiner_user_id_list, event_joiner_get, event_joiner_state, last_event_by_zsite_id
from model.po import po_new, STATE_RM
from zkit.jsdict import JsDict
from model.po_pic import pic_list_edit
from model.notice import notice_new
from model.po_question import mc_answer_id_get
from model.rank import rank_new
from model.txt import txt_new
from ctrl.zsite.po import PoBase



@urlmap('/po/event/(\d+)/state')
class EventState(LoginBase):
    def get(self, id):
        event = Event.mc_get(id)
        if event.id and event.zsite_id == self.current_user_id:
            if event.cid == EVENT_STATE_INIT:
                return self.redirect('/po/event/%s'%id)
            return self.render(event=event)
        self.redirect('/po/event')



@urlmap('/po/event')
@urlmap('/po/event/(\d+)')
class Index(LoginBase):
    def post(self, id=0):
        user_id = self.current_user_id

        if id:
            event = Event.mc_get(id)
            if event.zsite_id != self.current_user_id:
                return self.redirect('/%s'%id)
            can_change = event.can_change()
        else:
            event = None
            can_change = True

        event = po_event_edit_post(self, id, event, can_change, event_new_if_can_change)
        if event:
            if not id:
                id = event.id
                zsite = self.zsite
                zsite_id = zsite_id_by_zsite_user_id(zsite, user_id)
                po_new(CID_EVENT, user_id, '', STATE_SECRET, id=id, zsite_id=zsite_id)

            if event.state <= EVENT_STATE_TO_REVIEW:
                return self.redirect('/po/edit/%s'%id)
            else:
                return self.redirect('/%s'%id)

    def get(self, id=0):
        user_id = self.current_user_id

        if id:
            event = Event.mc_get(id)
            if not event or event.zsite_id != self.current_user_id:
                return self.redirect('/po/event')
            return po_event_edit_get(self, event)

        default_event = last_event_by_zsite_id(user_id)

        return self.render(errtip=Errtip(), default_event=default_event)


def po_event_edit_post(self, id, event, can_change, event_new):
    user_id = self.current_user_id
    if event:
        user_id = event.zsite_id
    errtip = Errtip()
    phone = self.get_argument('phone', '')
    address = self.get_argument('address', None)
    limit_up = self.get_argument('limit_up', '42')
    limit_down = self.get_argument('limit_down', '0')
    transport = self.get_argument('transport', '')
    price = self.get_argument('price', '0')
    pid = self.get_argument('pid', '1')
    event_cid = self.get_argument('event_cid', '')
    #print event_cid, "!!!!!!!!!!!"
    begin_time = self.get_argument('begin_time', '')
    end_time = self.get_argument('end_time', '')
    begin_time = self.get_argument('begin_time', '')

    begin_time_hour = self.get_argument('begin_time_hour', '0')
    begin_time_minute = self.get_argument('begin_time_minute', '0')
    end_time_hour = self.get_argument('end_time_hour', '0')
    end_time_minute = self.get_argument('end_time_minute', '0')

    if not can_change:
        city_pid = end = begin = None
    else:
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
            errtip.limit_down = '人数不能为负数'

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
            if not (o and o.cid == CID_EVENT):
                pic_id = None

    if not pic_id:
        errtip.pic = '请上传图片'

    if errtip:
        self.render(
            event=event,
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
            begin_time=begin_time if can_change else 0,
            end_time=end_time if can_change else 0,
            begin_time_hour=begin_time_hour,
            begin_time_minute=begin_time_minute,
            end_time_hour=end_time_hour,
            end_time_minute=end_time_minute,
        )
        return
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
        return event

def po_event_edit_get(self, event):
    return self.render(
        errtip=Errtip(),
        event_id=event.id,
        event=event,
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




@urlmap('/event/feedback/(\d+)')
class EventFeedback(PoBase):

    cid = CID_EVENT_FEEDBACK

    def po_save(self, user_id, name, txt, good, zsite_id):
        event = self.event
        po = po_event_feedback_new(
            user_id,
            name,
            txt,
            good,
            event.id,
            event.zsite_id
        )
        if txt:
            po.txt_set(txt)
        return po

    def _event(self, event_id):
        self.event_id = event_id
        self.event = event = Event.mc_get(event_id)
        current_user_id = self.current_user_id

        if not event:
            return self.redirect('/')

        if event.state < EVENT_STATE_NOW:
            return self.redirect(event.link)

        state = event_joiner_state(
            event_id, current_user_id
        )

        if state < EVENT_JOIN_STATE_YES:
            return self.redirect(event.link)

        return event

    def get(self, event_id):
        if not self._event(event_id):
            return

        current_user_id = self.current_user_id

        event_joiner = event_joiner_get(
            event_id, current_user_id
        )

        return super(EventFeedback, self).get()

    def post(self, event_id):
        if not self._event(event_id):
            return
        return super(EventFeedback, self).post()


