#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import ZsiteBase, LoginBase, XsrfGetBase, login
from ctrl._urlmap.zsite import urlmap
from config import SITE_HTTP, RPC_HTTP
from zkit.page import page_limit_offset
from model.event import Event, event_joiner_new, event_joiner_state, event_joiner_list, event_joiner_count
from model.event import event_count_by_zsite_id, event_join_count_by_user_id, event_open_count_by_user_id
from model.event import event_list_by_zsite_id, event_list_join_by_user_id, event_list_open_by_user_id
from model.event import EVENT_JOIN_STATE_NO, EVENT_JOIN_STATE_NEW, EVENT_JOIN_STATE_YES, EVENT_JOIN_STATE_END, EVENT_JOIN_STATE_REVIEW
from model.money import pay_event_new, TRADE_STATE_NEW, TRADE_STATE_ONWAY, TRADE_STATE_FINISH, pay_account_get, bank, Trade, trade_log, pay_notice, read_cent
from model.money_alipay import alipay_payurl, alipay_payurl_with_tax, alipay_cent_with_tax
from model.cid import CID_USER, CID_PAY_ALIPAY, CID_TRADE_EVENT
from ctrl.me.i import NameCardEdit


@urlmap('/event')
@urlmap('/event-(\d+)')
class EventHandle(ZsiteBase):
    def get(self, n=1):
        zsite_id = self.zsite_id
        current_user_id = self.current_user_id
        can_admin = zsite_id == current_user_id

        total = event_count_by_zsite_id(zsite_id, can_admin)
        page, limit, offset = page_limit_offset(
            '/event-%s',
            total,
            n,
            PAGE_LIMIT
        )
        li = event_list_by_zsite_id(zsite_id, can_admin, limit, offset)
        self.render(
            li=li,
            page=page,
        )


@urlmap('/event/all')
@urlmap('/event/all-(\d+)')
class EventJoin(ZsiteBase):
    def get(self, n=1):
        zsite_id = self.zsite_id

        total = event_join_count_by_user_id(zsite_id)
        page, limit, offset = page_limit_offset(
            '/event/all-%s',
            total,
            n,
            PAGE_LIMIT
        )
        li = event_list_join_by_user_id(zsite_id, limit, offset)
        self.render(
            li=li,
            page=page,
        )


@urlmap('/event/ing')
@urlmap('/event/ing-(\d+)')
class EventOpen(ZsiteBase):
    def get(self, n=1):
        zsite_id = self.zsite_id

        total = event_open_count_by_user_id(zsite_id)
        page, limit, offset = page_limit_offset(
            '/event/ing-%s',
            total,
            n,
            PAGE_LIMIT
        )
        li = event_list_open_by_user_id(zsite_id, limit, offset)
        self.render(
            li=li,
            page=page,
        )


class EventBase(LoginBase):
    def event(self, id):
        o = Event.mc_get(id)
        if o:
            if o.zsite_id == self.zsite_id:
                return o
            return self.redirect(o.link)
        return self.redirect('/')


@urlmap('/event/join/(\d+)')
class EventJoin(NameCardEdit, EventBase):
    def event(self, id):
        current_user_id = self.current_user_id
        event = super(EventJoin, self).event(id)
        if event:
            if not event.can_admin(current_user_id) and event_joiner_state(id, current_user_id) < EVENT_JOIN_STATE_NEW:
                return event
            return self.redirect(event.link)

    def get(self, id):
        event = self.event(id)
        if event is None:
            return

        return NameCardEdit.get(self)

    def post(self, id):
        event = self.event(id)
        if event is None:
            return

        if not self.save():
            return self.get(id)

        if event.cent:
            return self.redirect('/event/pay/%s' % id)

        event_joiner_new(id, self.current_user_id)
        return self.redirect(event.link)


@urlmap('/event/pay/(\d+)')
class EventPay(EventJoin):
    def event(self, id):
        event = super(EventPay, self).event(id)
        if event:
            if event.cent:
                return event
            return self.redirect(event.link)

    def cent_need(self, event):
        current_user_id = self.current_user_id
        cent = event.cent
        bank_cent = bank.get(current_user_id)
        if bank_cent >= cent:
            return 0
        elif bank_cent > 0:
            return cent - bank_cent
        return cent

    def get(self, id):
        event = self.event(id)
        if event is None:
            return

        cent_need = self.cent_need(event)

        return self.render(
            event=event,
            cent_need=cent_need,
        )

    def post(self, id):
        event = self.event(id)
        if event is None:
            return

        current_user_id = self.current_user_id
        zsite_id = self.zsite_id

        cent_need = self.cent_need(event)

        if cent_need:
            state = TRADE_STATE_NEW
        else:
            state = TRADE_STATE_ONWAY

        t = pay_event_new(event.cent/100.0, current_user_id, zsite_id, id, state)

        if not cent_need:
            event_joiner_new(id, current_user_id)
            return self.redirect(event.link)

        cent_with_tax = alipay_cent_with_tax(cent_need)

        subject = '参加****还需充值%s元(其中手续费%s)' % (read_cent(cent_with_tax), read_cent(cent_with_tax-cent_need))

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


PAGE_LIMIT = 42


@urlmap('/event/check/(\d+)')
@urlmap('/event/check/(\d+)-(\d+)')
class EventCheck(EventBase):
    def get(self, id, n=1):
        event = self.event(id)
        if event is None:
            return

        total = event_joiner_count(id)

        page, limit, offset = page_limit_offset(
            '/event/verify/%s-%%s' % id,
            total,
            n,
            PAGE_LIMIT
        )

        li = event_joiner_list(id, limit, offset)

        return self.render(
            event=event,
            event_joiner_list=li,
            page=page,
        )
