#!/usr/bin/env python
# -*- coding: utf-8 -*-
from yajl import dumps, loads
from time import time
from mail import rendermail
from _db import Model, McModel, McCache, McCacheA, McNum
from kv import Kv
from cid import CID_TRADE_CHARDE, CID_TRADE_WITHDRAW, CID_TRADE_PAY, CID_TRADE_DEAL, CID_TRADE_EVENT, CID_VERIFY_MONEY, CID_PAY_ALIPAY, CID_NOTICE_PAY
from zsite import Zsite
from user_mail import mail_by_user_id
from mail import rendermail
from verify import verify_new, verifyed
from state import STATE_APPLY, STATE_SECRET, STATE_ACTIVE
from zkit.attrcache import attrcache

mc_frozen_get = McCache('FrozenBank.%s')

def read_cent(cent):
    return ('%.2f' % (cent / 100.)).rstrip('0').rstrip('.')

# Bank
bank = Kv('bank', 0)

def bank_view(user_id):
    return read_cent(bank.get(user_id))

def bank_change(user_id, cent):
    gold = bank.get(user_id)
    bank.set(user_id, gold + cent)

def bank_can_pay(user_id, cent):
    assert cent > 0
    return bank.get(user_id) >= cent

# Trade
TRADE_CID_DICT = {
    CID_TRADE_CHARDE: '充值',
    CID_TRADE_WITHDRAW: '提现',
    CID_TRADE_DEAL: '交易',
    CID_TRADE_EVENT: '活动',
}

TRADE_STATE_NEW = 5
TRADE_STATE_ONWAY = 10
TRADE_STATE_ROLLBACK = 15
TRADE_STATE_FINISH = 20

class Trade(Model):
    link = '/money/bill'

    @property
    def log(self):
        return trade_log.get(self.id)

    @property
    def read_value(self):
        return read_cent(self.value)

    @property
    def read_tax(self):
        return read_cent(self.tax)

mc_frozen_get = McCache('FrozenBank.%s')

@mc_frozen_get('{user_id}')
def frozen_get(user_id):
    c = Trade.raw_sql('select sum(value) from trade where from_id=%s and state=%s', user_id, TRADE_STATE_ONWAY)
    c = c.fetchone()[0]
    if c:
        return int(c)
    return 0

def frozen_view(user_id):
    return read_cent(frozen_get(user_id))

def trade_new(cent, tax, from_id, to_id, cid, rid, state=TRADE_STATE_ONWAY, for_id=0):
    now = int(time())
    t = Trade(
        value=cent,
        tax=tax,
        from_id=from_id,
        to_id=to_id,
        cid=cid,
        rid=rid,
        state=state,
        create_time=now,
        update_time=now,
        for_id=for_id
    )
    t.save()
    if state == TRADE_STATE_ONWAY:
        bank_change(from_id, -cent)
        mc_frozen_get.delete(t.from_id)
    elif state == TRADE_STATE_FINISH:
        bank_change(from_id, -cent)
        bank_change(to_id, cent)
    return t

def trade_open(t):
    if t.state == TRADE_STATE_NEW:
        bank_change(t.from_id, -t.value)
        t.update_time = int(time())
        t.state = TRADE_STATE_ONWAY
        t.save()
        mc_frozen_get.delete(t.from_id)

def trade_finish(t):
    from_id = t.from_id
    to_id = t.to_id
    value = t.value
    state = t.state
    now = int(time())

    is_new = state == TRADE_STATE_NEW
    is_onway = state == TRADE_STATE_ONWAY
    if is_new:
        bank_change(from_id, -value)
    if is_new or is_onway:
        bank_change(to_id, value)
        t.update_time = now
        t.state = TRADE_STATE_FINISH
        t.save()
        if is_onway:
            mc_frozen_get.delete(from_id)

def trade_fail(t):
    from_id = t.from_id
    value = t.value
    state = t.state
    now = int(time())
    if state == TRADE_STATE_NEW:
        t.update_time = now
        t.state = TRADE_STATE_ROLLBACK
        t.save()
    elif state == TRADE_STATE_ONWAY:
        bank_change(from_id, value)
        t.update_time = now
        t.state = TRADE_STATE_ROLLBACK
        t.save()
        mc_frozen_get.delete(from_id)

def trade_history(user_id):
    qs = Trade.where(
        '(to_id=%%s and state=%s) or (to_id=%%s and cid=%s) or from_id=%%s' % (
            TRADE_STATE_FINISH,
            CID_TRADE_WITHDRAW,
        ),
        user_id,
        user_id,
        user_id,
    ).order_by('update_time desc')
    return list(qs)

# TradeLog
trade_log = Kv('trade_log')

# PayAccount
class PayAccount(Model):
    pass

def pay_account_new(user_id, account, name, cid):
    a = PayAccount.get_or_create(user_id=user_id, cid=cid)
    if account:
        a.account = account
    if name:
        a.name = name
    a.save()
    return a

def pay_account_get(user_id, cid):
    return pay_account_name_get(user_id, cid)[0]

def pay_account_name_get(user_id, cid):
    a = PayAccount.get(user_id=user_id, cid=cid)
    account = None
    name = None
    if a:
        account = a.account
        name = a.name
    if not account:
        account = mail_by_user_id(user_id)
    if not name:
        name = Zsite.mc_get(user_id).name
    return account, name

def pay_notice(pay_id):
    from notice import notice_new
    trade = Trade.get(pay_id)
    notice_new(trade.from_id, trade.to_id, CID_NOTICE_PAY, pay_id)
    t_log = (trade_log.get(pay_id))
    if t_log:
        message = loads(t_log)
        if 'txt' in message:
            if 'secret' in message:
                state = STATE_SECRET
            else:
                state = STATE_ACTIVE
            to_user = Zsite.mc_get(trade.to_id)
            from_user = Zsite.mc_get(trade.from_id)
            to_user.reply_new(from_user, message['txt'], state)


# Charge
CHARGE_TAX = {
    CID_PAY_ALIPAY: 0 , #1.5 / 100,
}

def charge_new(price, user_id, cid, for_id=0):
    assert price > 0
    cent = int(price * 100)
    tax = int(round(cent * CHARGE_TAX[cid]))
    t = trade_new(cent-tax, tax, 0, user_id, CID_TRADE_CHARDE, cid, TRADE_STATE_ONWAY, for_id)
    vid, ck = verify_new(user_id, CID_VERIFY_MONEY)
    return '%s_%s_%s' % (t.id, vid, ck)

def charged(out_trade_no, total_fee, rid, d):
    id, vid, ck = out_trade_no.split('_', 2)
    user_id, vcid = verifyed(vid, ck)
    if vcid == CID_VERIFY_MONEY:
        t = Trade.get(id)
        if t and t.to_id == user_id and t.rid == rid  and t.value + t.tax == int(float(total_fee)*100):
            if t.state == TRADE_STATE_ONWAY:
                trade_finish(t)
                trade_log.set(id, dumps(d))
                for_t = Trade.get(t.for_id)
                if for_t:
                    if bank_can_pay(for_t.from_id, for_t.value):
                        for_cid = for_t.cid
                        if for_cid == CID_TRADE_PAY:
                            trade_finish(for_t)
                            pay_notice(for_t.id)
                        elif for_cid == CID_TRADE_EVENT:
                            from event import event_joiner_state, event_joiner_new, EVENT_JOIN_STATE_NEW
                            event_id = for_t.rid
                            user_id = for_t.from_id
                            if event_joiner_state(event_id, user_id) < EVENT_JOIN_STATE_NEW:
                                trade_open(for_t)
                                event_joiner_new(event_id, user_id)
                            else:
                                trade_fail(for_t)
                                return t
                        return for_t
            return t

# Withdraw
def withdraw_new(price, user_id, cid):
    assert price > 0
    cent = int(price * 100)
    tax = int(round(cent * CHARGE_TAX[cid]))
    return trade_new(cent, tax, user_id, 0, CID_TRADE_WITHDRAW, cid, TRADE_STATE_ONWAY)

def withdraw_fail(id, txt):
    t = Trade.get(id)
    if t and t.cid == CID_TRADE_WITHDRAW and t.state == TRADE_STATE_ONWAY:
        trade_fail(t)
        trade_log.set(id, txt)
        mail = mail_by_user_id(id)
        rendermail(
            '/mail/notice/with_draw_fail.txt', mail,
            t.name, cid=t.cid, account=t.account,
            value=t.value/100.0
        )

def withdraw_success(id, trade_no):
    t = Trade.get(id)
    if t and t.cid == CID_TRADE_WITHDRAW and t.state == TRADE_STATE_ONWAY:
        trade_finish(t)
        trade_log.set(id, trade_no)
        mail = mail_by_user_id(id)
        rendermail(
            '/mail/notice/with_draw_success.txt', mail,
            t.name, cid=t.cid, account=t.account,
            value=t.value/100.0
        )

def withdraw_open_count():
    return Trade.where(cid=CID_TRADE_WITHDRAW, to_id=0, state=TRADE_STATE_ONWAY).count()

def withdraw_max():
    c = Trade.raw_sql('select max(id) from trade where cid=%s and to_id=%s', CID_TRADE_WITHDRAW, 0)
    return c.fetchone()[0] or 0

def withdraw_list():
    qs = Trade.where(cid=CID_TRADE_WITHDRAW, to_id=0, state=TRADE_STATE_ONWAY).order_by('id desc')
    for i in qs:
        i.account, i.name = pay_account_name_get(i.from_id, i.rid)
    return qs


# Deal
def pay_new(price, from_id, to_id, rid, state=TRADE_STATE_NEW):
    assert price > 0
    cent = int(price * 100)
    return trade_new(cent, 0, from_id, to_id, CID_TRADE_PAY, rid, state)

def deal_new(price, from_id, to_id, rid, state=TRADE_STATE_ONWAY):
    assert price > 0
    cent = int(price * 100)
    return trade_new(cent, 0, from_id, to_id, CID_TRADE_DEAL, rid, state)


# Event
def pay_event_new(price, from_id, to_id, rid, state=TRADE_STATE_NEW):
    assert price > 0
    cent = int(price * 100)
    return trade_new(cent, 0, from_id, to_id, CID_TRADE_EVENT, rid, state)

def pay_event_get(event, user_id):
    li = Trade.where(from_id=user_id, to_id=event.zsite_id, rid=event.id, state=TRADE_STATE_ONWAY)
    if li:
        for i in li[1:]:
            trade_fail(i)
        return li[0]


if __name__ == '__main__':
    pass

    t = Trade.get(127)
    print t.cid, t.for_id


