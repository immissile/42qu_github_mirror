#!/usr/bin/env python
# -*- coding: utf-8 -*-
from zkit.money import Alipay
from config import ALIPAY_ID, ALIPAY_SALT, ALIPAY_EMAIL

ALIPAY = Alipay(ALIPAY_SALT, ALIPAY_ID, ALIPAY_EMAIL)

def _alipay_payurl(
        user_id, total_fee, return_url, notify_url, subject, buyer_email=None
    ):
    if buyer_email is None:
        buyer_email = user_mail_get(user_id) or ''
    out_trade_no = pay_new(man_id, total_fee)
    body = "%s -付款-> %s -跳转-> %s"%(buyer_email, man_id, return_url)
    return ALIPAY.payurl(
        total_fee,
        out_trade_no,
        subject,
        return_url,
        notify_url,
        buyer_email,
        body
    )

def alipay_payurl(
        man_id, total_fee, return_url, notify_url, subject, buyer_email=None
    ):
    total_fee = int(float(total_fee)*100)/100.0
    return _alipay_payurl(
        man_id,
        total_fee,
        return_url,
        notify_url,
        subject,
        buyer_email
    )

def alipay_payurl_with_tax(
        man_id, total_fee, return_url, notify_url, subject, buyer_email=None
    ):
    total_fee = int(float(total_fee)*100)/100.0
    _total_fee = int(int(float(total_fee)*100+0.5)/ALIPAY_TAX)/100.0
    alipay_tax = _total_fee - total_fee
    if alipay_tax:
        subject += ' (支付宝手续费%s)' % alipay_tax
    return _alipay_payurl(
        man_id,
        _total_fee,
        return_url,
        notify_url,
        subject,
        buyer_email
    )

def alipay_url_recall(url):
    #'WAIT_BUYER_PAY':'等待买家付款',
    #'WAIT_SELLER_CONFIRM_TRADE':'交易已创建，等待卖家确认',
    #'WAIT_SYS_CONFIRM_PAY':'确认买家付款中，暂勿发货',
    #'WAIT_SELLER_SEND_GOODS':'支付宝收到买家付款，请卖家发货',
    #'WAIT_BUYER_CONFIRM_GOODS':'卖家已发货，买家确认中',
    #'WAIT_SYS_PAY_SELLER':'买家确认收到货，等待支付宝打款给卖家',
    #'TRADE_FINISHED':'交易成功结束',
    #'TRADE_CLOSED':'交易中途关闭（未完成）',
    d = alipay_url_parse(url)
    dd = dict(d)
    return alipay_recall(dd)

def alipay_recall(dd):
    if dd.get('trade_status') not in ("TRADE_FINISHED", "TRADE_SUCCESS"):
        return

    result = ALIPAY.recall_valid(dd)
    if not result:
        return False

    #如果验证有效 , 下面的参数肯定有
    trade_no = dd['trade_no']
    out_trade_no = dd['out_trade_no']
    total_fee = dd['total_fee']
    return pay_charged(trade_no, out_trade_no, total_fee, CID_BANK_ALIPAY)
