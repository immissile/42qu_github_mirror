#!/usr/bin/env python
# -*- coding: utf-8 -*-
from yajl import dumps, loads
from time import time
from _db import Model, McModel, McCache, McCacheA, McLimitA, McNum
from kv import Kv
from cid import CID_TRADE_CHARDE, CID_TRADE_WITHDRAW, CID_TRADE_DONATE, CID_TRADE_DEAL, CID_TRADE_REWARD, CID_VERIFY_MONEY, CID_PAY_ALIPAY
from zsite import Zsite
from user_mail import mail_by_user_id
from verify import verify_new, verifyed

def read_cent(cent):
    return '%.2f' % (cent / 100.)

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
TRADE_CID_DIC = {
    CID_TRADE_CHARDE: '充值',
    CID_TRADE_WITHDRAW: '提现',
    CID_TRADE_DEAL: '交易',
#    CID_TRADE_REWARD: '奖励',
}

TRADE_STATE_NEW = 5
TRADE_STATE_OPEN = 10
TRADE_STATE_FAIL = 15
TRADE_STATE_FINISH = 20

class Trade(Model):
    def open(self):
        trade_open(self)

    def finish(self):
        trade_finish(self)

    def fail(self):
        trade_fail(self)

    @property
    def got(self):
        return read_cent(self.value)

    @property
    def taxes(self):
        return read_cent(self.tax)

mc_frozen_bank = McCache('FrozenBank.%s')

@mc_frozen_bank('{user_id}')
def frozen_bank(user_id):
    c = Trade.raw_sql('select sum(cent) from trade where from_id=%s and state=%s', user_id, TRADE_STATE_OPEN)
    return c.fetchone()[0] or 0

def frozen_view(user_id):
    return read_cent(frozen_bank(user_id))

def trade_new(cent, tax, from_id, to_id, cid, rid, state=TRADE_STATE_OPEN, for_id=0):
    create_time = int(time())
    t = Trade(
        value=cent,
        tax=tax,
        from_id=from_id,
        to_id=to_id,
        cid=cid,
        rid=rid,
        state=state,
        create_time=create_time,
        update_time=create_time,
        for_id=for_id
    )
    t.save()
    if state == TRADE_STATE_OPEN:
        bank_change(from_id, -cent)
        mc_frozen_bank.delete(t.from_id)
    elif state == TRADE_STATE_FINISH:
        bank_change(from_id, -cent)
        bank_change(to_id, cent)
    return t

def trade_open(t):
    if t.state == TRADE_STATE_NEW:
        bank_change(t.from_id, -t.value)
        t.update_time = int(time())
        t.state = TRADE_STATE_OPEN
        t.save()
        mc_frozen_bank.delete(t.from_id)

def trade_finish(t):
    from_id = t.from_id
    to_id = t.to_id
    value = t.value
    state = t.state
    update_time = int(time())
    if state == TRADE_STATE_NEW:
        bank_change(from_id, -value)
        bank_change(to_id, value)
        t.update_time = update_time
        t.state = TRADE_STATE_FINISH
        t.save()
    elif state == TRADE_STATE_OPEN:
        bank_change(to_id, value)
        t.update_time = update_time
        t.state = TRADE_STATE_FINISH
        t.save()
        mc_frozen_bank.delete(from_id)

def trade_fail(t):
    from_id = t.from_id
    value = t.value
    state = t.state
    update_time = int(time())
    if state == TRADE_STATE_NEW:
        t.update_time = update_time
        t.state = TRADE_STATE_FAIL
        t.save()
    elif state == TRADE_STATE_OPEN:
        bank_change(from_id, value)
        t.update_time = update_time
        t.state = TRADE_STATE_FAIL
        t.save()
        mc_frozen_bank.delete(from_id)

def trade_history(user_id):
    qs = Trade.where('(to_id=%%s and not (cid=%s and state<%s)) or from_id=%%s' % (CID_TRADE_CHARDE, TRADE_STATE_FINISH), user_id, user_id).order_by('update_time desc')
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

# Charge
CHARGE_TAX = {
    CID_PAY_ALIPAY: 1.5 / 100,
}

def charge_new(price, user_id, cid, for_id=0):
    assert price > 0
    cent = int(price * 100)
    tax = int(round(cent * CHARGE_TAX[cid]))
    t = trade_new(cent-tax, tax, 0, user_id, CID_TRADE_CHARDE, cid, TRADE_STATE_OPEN, for_id)
    vid, ck = verify_new(user_id, CID_VERIFY_MONEY)
    return '%s_%s_%s' % (t.id, vid, ck)

def charged(out_trade_no, total_fee, rid, d):
    id, vid, ck = out_trade_no.split('_', 2)
    user_id, vcid = verifyed(vid, ck)
    if vcid == CID_VERIFY_MONEY:
        t = Trade.get(id)
        if t and t.to_id == user_id and t.rid == rid  and t.value + t.tax == int(float(total_fee)*100):
            if t.state == TRADE_STATE_OPEN:
                t.finish()
                trade_log.set(user_id, dumps(d))
                if t.for_id:
                    for_t = Trade.get(t.for_id)
                    if bank_can_pay(for_t.from_id, for_t.value):
                        for_t.open()
                        for_t.finish()
                        return for_t
            return t

# Withdraw
def withdraw_new(price, user_id, cid):
    assert price > 0
    cent = int(price * 100)
    tax = int(round(cent * CHARGE_TAX[cid]))
    return trade_new(cent, tax, user_id, 0, CID_TRADE_WITHDRAW, cid, TRADE_STATE_OPEN)

def withdraw_fail(id, txt):
    t = Trade.get(id)
    if t and t.cid == CID_TRADE_WITHDRAW and t.state == TRADE_STATE_OPEN:
        t.fail()
        trade_log.set(id, txt)

def withdraw_open_count():
    return Trade.where(cid=CID_TRADE_WITHDRAW, to_id=0, state=TRADE_STATE_OPEN).count()

def withdraw_max():
    c = Trade.raw_sql('select max(id) from trade where cid=%s and to_id=%s', CID_TRADE_WITHDRAW, 0)
    return c.fetchone()[0] or 0

def withdraw_list():
    qs = Trade.where(cid=CID_TRADE_WITHDRAW, to_id=0, state=TRADE_STATE_OPEN).order_by('id desc')
    for i in qs:
        i.account, i.name = pay_account_name_get(i.from_id, i.rid)
    return qs

# Deal
def donate_new(price, from_id, to_id, rid, state=TRADE_STATE_NEW):
    assert price > 0
    cent = int(price * 100)
    t = trade_new(cent, 0, from_id, to_id, CID_TRADE_DONATE, rid, state)
    return t.id

def deal_new(price, from_id, to_id, rid, state=TRADE_STATE_OPEN):
    assert price > 0
    cent = int(price * 100)
    return trade_new(cent, 0, from_id, to_id, CID_TRADE_DEAL, rid, state)
