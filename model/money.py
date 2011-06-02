#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time
from _db import Model, McModel, McCache, McCacheA, McLimitA, McNum
from kv import Kv
from cid import CID_TRADE_CHARDE, CID_TRADE_WITHDRAW, CID_TRADE_DEAL, CID_TRADE_REWARD, CID_TRADE_TAX
from zsite import Zsite
from user_mail import mail_by_user_id

# Bank
bank = Kv('bank', 0)

def bank_view(user_id):
    return '%.2f' % (bank.get(user_id) / 100.)

def bank_change(user_id, cent):
    gold = bank.get(user_id)
    bank.set(user_id, gold + cent)

def bank_can_pay(user_id, cent):
    assert cent > 0
    return bank.get(user_id) >= cent

# Trade
TRADE_CID_DIC = {
    CID_TRADE_CHARDE: '充值',
    CID_TRADE_WITHDRAW: '体现',
    CID_TRADE_DEAL: '交易',
#    CID_TRADE_REWARD: '奖励',
#    CID_TRADE_TAX: '税收',
}

TRADE_STATE_OPEN = 1
TRADE_STATE_CANCEL = 5
TRADE_STATE_FINISH = 9

class Trade(Model):
    finish = trade_finish
    cancel = trade_cancel

    @property
    def view(self):
        return '%.2f' % self.value

mc_frozen_bank = McCache('FrozenBank.%s')

@mc_frozen_bank('{user_id}')
def frozen_bank(user_id):
    c = Trade.raw_sql('select sum(cent) from trade where from_id=%s and state=%s', user_id, STATE_OPEN)
    return c.fetchone()[0] or 0

def frozen_view(user_id):
    return '%.2f' % (frozen_bank(user_id) / 100.)

def _trade_new(cent, from_id, to_id, cid, rid, state):
    t = int(time())
    t = Trade(
        value=cent,
        from_id=from_id,
        to_id=to_id,
        cid=cid,
        rid=rid,
        state=state,
        create_time=t,
        update_time=t,
    )
    t.save()
    return t

def trade_new(price, from_id, to_id, cid, rid, state=TRADE_STATE_OPEN):
    assert yuan > 0
    cent = int(100 * price)
    t = _trade_new(cent, from_id, to_id, cid, rid, state)
    bank_change(from_id, -cent)
    if state == TRADE_STATE_FINISH:
        bank_change(to_id, cent)
    return t

def trade_finish(t):
    if t.state == TRADE_STATE_OPEN:
        bank_change(t.to_id, t.cent)
        t.update_time = int(time())
        t.state = TRADE_STATE_FINISH
        t.save()
        mc_frozen_bank.delete(t.from_id)

def trade_cancel(t):
    if t.state == TRADE_STATE_OPEN:
        from_id = t.from_id
        bank_change(from_id, t.cent)
        t.update_time = int(time())
        t.state = TRADE_STATE_CANCEL
        t.save()
        mc_frozen_bank.delete(from_id)

def trade_history(user_id):
    pass

# TradeLog
trade_log = Kv('trade_log')
#class TradeLog(Model):
#    pass


# PayAccount
class PayAccount(Model):
    pass

def pay_account_new(user_id, account, name, cid):
    a = DrawAccount.get_or_create(user_id=user_id, cid=cid)
    if account:
        a.account = account
    if name:
        a.name = name
    a.save()
    return a

def pay_account_get(user_id, cid):
    a = DrawAccount.get(user_id=user_id, cid=cid)
    if a:
        return account, name
    return mail_by_user_id(user_id), Zsite.mc_get(user_id).name


mc_bank_price = McCache('BankPrice:%s')
mc_pay_on_way_to_total = McCache('PayOnwayTo:%s')
mc_pay_on_way_from_total = McCache('PayOnwayFrom:%s')

CID_BANK_ALIPAY = 1
CID2CN = {
    CID_BANK_ALIPAY: '支付宝',
}
CID_PAY_TAX = {
    CID_BANK_ALIPAY: 1.5,
}
CID_DRAW_TAX = {
    CID_BANK_ALIPAY: 1.5,
}

ALIPAY_TAX = float(100 - CID_PAY_TAX[CID_BANK_ALIPAY])/100

class DrawAccount(Model):
    pass

class DrawOrder(Model):
    @property
    def real(self):
        return int(self.price*(1-(CID_DRAW_TAX[self.cid]/100.0))-1)

class PayOrder(Model):
    pass

class Payed(Model):
    pass


class PayLog(Model):
    pass

class PayOnway(McModel):
    pass

def draw_order_new(man_id, price, cid):
    htm = '%s提现'%(CID2CN[cid])
    DrawOrder.begin()
    ow = pay_onway_new(man_id, 0, price, htm)
    if ow:
        order = DrawOrder(
            price=int(price*100),
            man_id=man_id,
            state=STATE_OPEN,
            cid=cid,
            pay_onway_id=ow.id
        )
        order.save()
    DrawOrder.commit()
    return order

def pay_onway_id2log(id):
    ow = PayOnway.get(id)
    if ow:
        return pay_onway2log(ow)

def pay_onway2log(ow):
    if ow.state != STATE_CLOSE:
        ow.state = STATE_CLOSE
        ow.save()
        from_id = ow.from_id
        to_id = ow.to_id
        price = ow.price
        if from_id:
            htm = ow.htm
            log = PayLog(to_id=from_id, price=-price, htm=htm, from_id=to_id)
            log.save()
            mc_pay_on_way_from_total.delete(from_id)
        if to_id:
            htm = ow.htm
            bank_price_change_by_man_id(to_id, price/100.0, htm, from_id)
            mc_pay_on_way_to_total.delete(to_id)
    return ow

def draw_order_rollback(id):
    DrawOrder.begin()
    order = DrawOrder.get(id)
    if order:
        man_id = order.man_id
        cid = order.cid
        ow = PayOnway.get(order.pay_onway_id)
        if ow:
            ow.state = STATE_CLOSE
            ow.save()
        order.trade_no = ''
        order.state = STATE_CLOSE
        order.update_time = datetime.now()
        order.save()
        bank_price_change(man_id, order.price, 1)
        mc_pay_on_way_from_total.delete(man_id)
    DrawOrder.commit()
    return order

def draw_order_close(id, trade_no):
    DrawOrder.begin()
    order = DrawOrder.get(id)
    if order and trade_no:
        man_id = order.man_id
        cid = order.cid
        pay_onway_id2log(order.pay_onway_id)
        order.trade_no = trade_no
        order.state = STATE_CLOSE
        order.update_time = datetime.now()
        order.save()

    DrawOrder.commit()
    #TODO

def draw_account_new(man_id, account, name, cid):
    a = DrawAccount.get_or_create(man_id=man_id, cid=cid)
    if account:
        a.account = account
    if name:
        a.name = name
    a.save()
    return a

def draw_account_get(man_id, cid):
    a = DrawAccount.get(man_id=man_id, cid=cid)
    account = None
    name = None
    if a:
        name = a.name
        account = a.account
    if not (account or name):
        if not name:
            man = Man.mc_get(man_id)
            name = man.name
        if not account:
            account = man_mail_get(man_id)
    return account, name

def pay_onway_from_total(id):
    return price_by_mc(
        PayOnway,
        'select sum(price) from pay_onway where from_id=%%s and state=%s'%STATE_OPEN,
        id,
        mc_pay_on_way_from_total
    )

def pay_onway_to_total(id):
    return price_by_mc(
        PayOnway,
        'select sum(price) from pay_onway where to_id=%%s and state=%s'%STATE_OPEN,
        id,
        mc_pay_on_way_to_total
    )

def bank_price_by_man_id(id):
    return price_by_mc(
        Bank,
        'select price from bank where id=%s',
        id,
        mc_bank_price
    )

def price_by_mc(model, sql, id, mc):
    s = mc.get(id)
    if s is None:
        c = model.raw_sql(sql, id)
        s = c.fetchone()
        if s:
            s = s[0]
        if s:
            s = int(s)
        else:
            s = 0
        mc.set(id, s)
    return s/100.0

def draw_order_state_open_total():
    return DrawOrder.where(state=STATE_OPEN).count()

def draw_order_by_state(state=STATE_OPEN):
    t = DrawOrder.where(state=state).order_by('id desc')
    for i in t:
        man_id = i.man_id
        cid = i.cid
        account, name = draw_account_get(man_id, cid)
        i.account = account
        i.name = name
    return t

def pay_onway_new(from_id, to_id, price, htm, max_day=None):
    if not price:
        return
    create_time = datetime.now()
    o = PayOnway(
        from_id=from_id,
        to_id=to_id,
        price=int(price*100),
        htm=htm,
        state=STATE_OPEN,
        create_time=create_time,
    )
    if max_day:
        o.expire_time = create_time+timedelta(max(int(max_day), 1))
    PayOnway.begin()

    bank_price_change(from_id, -price)

    o.save()
    PayOnway.commit()
    if from_id:
        mc_pay_on_way_from_total.delete(from_id)
    if to_id:
        mc_pay_on_way_to_total.delete(to_id)
    return o

def bank_price_change(man_id, price, rate=100):
    price = int(price*rate)
    bank = Bank.get(man_id)
    if not bank:
        bank = Bank(id=man_id, price=0)
    bank.price += price
    bank.save()
    mc_bank_price.delete(man_id)
    return bank

def bank_transfer(from_id, to_id, price, htm='', rate=100):
    price = price*rate
    Bank.begin()
    log = PayLog(
        from_id=to_id,
        to_id=from_id,
        price=-price,
        htm=htm
    )
    log.save()
    log = PayLog(
        from_id=from_id,
        to_id=to_id,
        price=price,
        htm=htm
    )
    log.save()

    if from_id:
        bank_price_change(from_id, -price, 1)
    if to_id:
        bank_price_change(to_id, price, 1)
    Bank.commit()

def bank_price_change_by_man_id(man_id, price, htm='', from_id=0):
    bank = bank_price_change(man_id, price)
    log = PayLog(to_id=man_id, price=int(price*100), htm=htm, from_id=from_id)
    log.save()
    return bank.price

def pay_log(man_id):
    #TODO 翻页
    plist = PayLog.where(to_id=man_id).order_by('id desc')
    return tuple(
        (i.price/100.0, i.htm, i.create_time, i.from_id, i.to_id) for i in plist
    )

def pay_onway_to(man_id, state=STATE_OPEN):
    plist = PayOnway.where(to_id=man_id, state=state).order_by('id desc')
    return tuple(
        (i.price/100.0, i.htm, i.create_time, i.from_id, i.to_id) for i in plist
    )

def pay_onway_from(man_id, state=STATE_OPEN):
    plist = PayOnway.where(from_id=man_id, state=state).order_by('id desc')
    return tuple(
        (i.price/100.0, i.htm, i.create_time, i.from_id, i.to_id) for i in plist
    )

def pay(man_id, price, cid):
    price = int(price*100)
    tax = int(price*CID_PAY_TAX[cid]/100.0)
    real = price - tax

    payed = Payed(man_id=man_id, cid=cid)
    payed.price = price
    payed.real = real
    bank_price_change_by_man_id(man_id, real/100.0, '%s付款'%CID2CN[cid])
    payed.save()
    return payed

def pay_new(man_id, total_fee):
    order = pay_order_new(man_id, total_fee)
    id = order.id
    uhx = order.uhx
    return '%s_%s_%s_%s'%(id, man_id, total_fee, uhx)

def pay_order_new(man_id, total_fee):
    uhx = uuid4().hex
    order = PayOrder(
        man_id=man_id,
        price=int(float(total_fee)*100),
        uhx=uhx,
        state=STATE_OPEN
    )

    order.save()
    return order

def pay_charged(trade_no, out_trade_no, total_fee, cid):
    id, man_id, total_fee, uhx = out_trade_no.split('_', 3)
    order = PayOrder.get(id)
    if not order:
        return
    man_id = int(man_id)
    total_fee = int(float(total_fee)*100)

    if order.state != STATE_OPEN:
        return
    if not (order.man_id == man_id and order.uhx == uhx and order.price==total_fee):
        return

    order.state = STATE_CLOSE
    order.trade_no = trade_no
    PayOrder.begin()
    order.save()
    payed = pay(man_id, total_fee/100.0, cid)
    PayOrder.commit()
    return payed
