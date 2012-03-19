#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import ZsiteBase, LoginBase, login
from ctrl._urlmap.zsite import urlmap
from config import SITE_HTTP, RPC_HTTP
from zkit.page import page_limit_offset
from model.event import Event, EVENT_STATE_RM, event_joiner_new, event_joiner_state, event_joiner_list, event_joiner_user_list,\
event_count_by_zsite_id, event_join_count_by_user_id,\
event_list_by_zsite_id, event_list_join_by_user_id,\
EVENT_JOIN_STATE_NO, EVENT_JOIN_STATE_NEW, EVENT_JOIN_STATE_YES, EVENT_JOIN_STATE_END, EVENT_STATE_BEGIN, EVENT_STATE_END
from model.money import pay_event_new, TRADE_STATE_NEW, TRADE_STATE_ONWAY, TRADE_STATE_FINISH, pay_account_get, bank, Trade, trade_log, pay_notice, read_cent
from model.money_alipay import alipay_payurl, alipay_payurl_with_tax, alipay_cent_with_tax
from model.cid import CID_USER, CID_PAY_ALIPAY, CID_TRADE_EVENT, CID_EVENT, CID_SITE
from ctrl.me.i import NameCardEdit
from model.zsite import ZSITE_STATE_VERIFY
from model.zsite_url import link, id_by_url
from config import SITE_DOMAIN
from model.site_po import feed_po_list_by_zsite_id, po_cid_count_by_zsite_id
#from model.sync import mq_sync_join_event_by_zsite_id


@urlmap('/event/to_review')
@urlmap('/event/to_review-(\d+)')
class EventMine(ZsiteBase):
    def get(self, n=1):
        zsite_id = self.zsite_id
        current_user_id = self.current_user_id
        if current_user_id != zsite_id:
            return self.redirect('/event')

        can_admin = zsite_id == current_user_id

        total = event_count_by_zsite_id(zsite_id, can_admin)
        page, limit, offset = page_limit_offset(
            '/event/to_review-%s',
            total,
            n,
            PAGE_LIMIT
        )
        li = event_list_by_zsite_id(zsite_id, can_admin, limit, offset)
        self.render(
            li=li,
            total=total,
            cid=CID_EVENT,
            page=page,
        )



@urlmap('/event')
@urlmap('/event-(\d+)')
class EventJoined(ZsiteBase):
    def get(self, n=1):
        zsite = self.zsite
        zsite_id = self.zsite_id
        user_id = self.current_user_id
        cid = CID_EVENT

        if zsite.cid == CID_SITE:
            total = po_cid_count_by_zsite_id(zsite_id, cid)
            template = '/ctrl/zsite/po_view/site_po_page.htm'
        else:
            total = event_join_count_by_user_id(zsite_id)
            template = 'ctrl/zsite/event/event_page.htm'


        page, limit, offset = page_limit_offset(
            '/event-%s',
            total,
            n,
            PAGE_LIMIT
        )

        if zsite.cid == CID_SITE:
            li = feed_po_list_by_zsite_id(user_id, zsite_id, cid, limit, offset)
        else:
            li = event_list_join_by_user_id(zsite_id, limit, offset)

        self.render(
            template,
            li=li,
            cid=cid,
            page=page,
            total=total,
        )


class EventBase(LoginBase):
    def _event(self, id):
        o = Event.mc_get(id)
        if o and o.state > EVENT_STATE_RM:
            if o.zsite_id == self.zsite_id:
                return o
            return self.redirect(link(o.zsite_id)+self.request.path)
        return self.redirect('/')


@urlmap('/event/(\d+)/state')
class EventState(EventBase):
    def get(self, id):
        event = self._event(id)
        if not event:
            return
        if event.state < EVENT_STATE_BEGIN:
            return self.redirect('/')
        current_user_id = self.current_user_id
        state = event_joiner_state(id, current_user_id)
        if state < EVENT_JOIN_STATE_NEW:
            return self.redirect('/%s'%id)

        return self.render(event=event, state=state)

def _event(self, id):
    current_user = self.current_user
    if current_user.state < ZSITE_STATE_VERIFY:
        return self.redirect('/i/verify')
    current_user_id = self.current_user_id
    self.event = event = EventBase._event(self, id)
    self.error = []
    if event:
        if event.zsite_id == current_user_id:
            return self.redirect('/event/check/%s'%id)
        if event.state == EVENT_STATE_END:
            return self.redirect(event.link)
        if event_joiner_state(id, current_user_id) < EVENT_JOIN_STATE_NEW:
            return event
        event_link = '/event/%s/state'%event.id
        return self.redirect(event_link)

@urlmap('/event/join/(\d+)')
class EventJoin(NameCardEdit, EventBase):
    _event = _event
    def get(self, id):
        event = self._event(id)
        if event is None:
            return
        return NameCardEdit.get(self)

    def post(self, id):
        event = self._event(id)
        if event is None:
            return

        event_link = '/event/%s/state'%event.id

        pid_now = self.get_argument('pid_now', None)
        name = self.get_argument('name', '')
        phone = self.get_argument('phone', '')
        mail = self.get_argument('mail', '')
        address = self.get_argument('address', '')

        error = self.error
        pid_now = int(pid_now)


        if not pid_now or int(pid_now) == 1:
            error.append('请选择现居城市')
        if not name:
            error.append('请输入本人姓名')
        if not phone:
            error.append('请填写手机号码')
        if not mail:
            error.append('请补充邮件地址')

        if not self.save() or error:
            return NameCardEdit.get(self)

        if event.cent:
            return self.redirect('/event/pay/%s' % id)

        current_user_id = self.current_user_id
        event_joiner_new(id, current_user_id)
        #mq_sync_join_event_by_zsite_id(current_user_id, id)
        return self.redirect(event_link)


@urlmap('/event/pay/(\d+)')
class EventPay(EventBase):
    def _event(self, id):
        event = _event(self, id)
        if event:
            if event.cent:
                return event
            return self.redirect(event.link)

    def cent_need(self):
        event = self.event
        current_user_id = self.current_user_id
        cent = event.cent
        bank_cent = bank.get(current_user_id)
        if bank_cent >= cent:
            return 0
        elif bank_cent > 0:
            return cent - bank_cent
        return cent

    def get(self, id):
        event = self._event(id)
        if event is None:
            return

        cent_need = self.cent_need()

        return self.render(
            event=event,
            cent_need=cent_need,
        )

    def post(self, id):
        event = self._event(id)
        if event is None:
            return

        event_link = '/event/%s/state'%event.id

        current_user_id = self.current_user_id
        zsite_id = self.zsite_id

        cent_need = self.cent_need()

        if cent_need:
            state = TRADE_STATE_NEW
        else:
            state = TRADE_STATE_ONWAY

        t = pay_event_new(event.cent/100.0, current_user_id, zsite_id, id, state)

        if not cent_need:
            event_joiner_new(id, current_user_id)
            return self.redirect(event_link)

        cent_with_tax = alipay_cent_with_tax(cent_need)

        subject = '报名活动 需充值%s元 ( 其中 : 手续费%s )' % (read_cent(cent_with_tax), read_cent(cent_with_tax-cent_need))

        return_url = '%s/money/alipay_sync' % SITE_HTTP
        notify_url = '%s/money/alipay_async' % RPC_HTTP

        alipay_account = pay_account_get(current_user_id, CID_PAY_ALIPAY)

        alipay_url = alipay_payurl_with_tax(
            current_user_id,
            cent_with_tax/100.0,
            return_url,
            notify_url,
            subject,
            alipay_account,
            t.id,
        )
        return self.redirect(alipay_url)


class EventAdmin(EventBase):
    def _event(self, id):
        current_user_id = self.current_user_id
        self.event = event = super(EventAdmin, self)._event(id)
        if event:
            if event.can_admin(current_user_id):
                return event
            return self.redirect(event.link)


@urlmap('/event/add/(\d+)')
class EventAdd(EventAdmin):
    def get(self, id):
        event = self._event(id)
        if event is None:
            return
        self.render(po=event.po)

    def post(self, id):
        event = self._event(id)
        if event is None:
            return
        txt = self.get_argument('txt', '')
        li = []
        for i in txt.splitlines():
            url = i.split('//')[-1].split('.%s' % SITE_DOMAIN)[0]
            if url.isdigit():
                user_id = int(url)
            else:
                user_id = id_by_url(url)
            if user_id and user_id not in li:
                li.append(user_id)
                event_joiner_new(id, user_id, EVENT_JOIN_STATE_YES)
        self.redirect('/event/add/%s' % id)


PAGE_LIMIT = 42

@urlmap('/event/check/(\d+)')
@urlmap('/event/check/(\d+)-(\d+)')
class EventCheck(EventAdmin):
    def get(self, id, n=1):
        event = self._event(id)
        if event is None:
            return

        total = event.join_count

        page, limit, offset = page_limit_offset(
            '/event/check/%s-%%s' % id,
            total,
            n,
            PAGE_LIMIT
        )

        li, pos_id = event_joiner_list(id, limit, offset)
        return self.render(
            event_joiner_list=li,
            pos_id=pos_id,
            page=page,
        )

@urlmap('/event/(\d+)/joiner/(\d+)')
class EventJoiner(EventBase):
    def get(self, id, n):
        event = self._event(id)
        if not event:
            return
        if event.state < EVENT_STATE_BEGIN:
            return self.redirect('/')
        total = event.join_count
        n = int(n)
        link_base = '/event/%s/joiner/%%s' % id
        li = event_joiner_user_list(id, 1, n-1)
        if li:
            self.render(
                po=event.po,
                user=li[0],
                total=total,
                n=n,
                link_base=link_base,
            )
        else:
            self.redirect(event.link)
