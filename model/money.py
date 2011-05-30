#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McCacheA, McLimitA, McNum
STATE_OPEN = 1
STATE_CLOSE = 0

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

class Bank(Model):
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
