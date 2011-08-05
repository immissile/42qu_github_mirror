#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import ZsiteBase, LoginBase, XsrfGetBase, login
from ctrl._urlmap.zsite import urlmap
from config import SITE_HTTP, RPC_HTTP
from model.state import STATE_DEL, STATE_APPLY, STATE_SECRET, STATE_ACTIVE
from model.event import Event, event_user_new, event_user_state
from model.money import pay_event_new, TRADE_STATE_NEW, TRADE_STATE_ONWAY, TRADE_STATE_FINISH, pay_account_get, bank, Trade, trade_log, pay_notice, read_cent
from model.money_alipay import alipay_payurl, alipay_payurl_with_tax, alipay_cent_with_tax
from model.cid import CID_USER, CID_PAY_ALIPAY, CID_TRADE_EVENT


class EventBase(LoginBase):
    def event(self, id):
        o = Event.mc_get(id)
        if o:
            if o.zsite_id == self.zsite_id:
                return o
            return self.redirect(o.link)
        return self.redirect('/')

    def get(self, id):
        event = self.event(id)
        if event is None:
            return

        return self.render(
            event=event,
        )


@urlmap('/event/join/(\d+)')
class EventJoin(EventBase):
    def event(self, id):
        current_user_id = self.current_user_id
        event = super(EventJoin, self).event(id)
        if event:
            if event_user_state(id, current_user_id) < STATE_APPLY:
                return event
            return self.redirect(event.link)

    def post(self, id):
        event = self.event(id)
        if event is None:
            return

        if event.cent:
            return self.redirect('/event/pay/%s' % id)

        event_user_new(id, current_user_id)
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
            event_user_new(id, current_user_id)
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
