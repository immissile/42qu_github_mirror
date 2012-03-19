#!/usr/bin/env python
# -*- coding: utf-8 -*-
from money import charge_new, charged, CHARGE_TAX
from cid import CID_PAY_ALIPAY
from user_mail import mail_by_user_id
from zkit.money import Alipay, alipay_url_parse
from config import ALIPAY_ID, ALIPAY_SALT, ALIPAY_EMAIL

ALIPAY = Alipay(ALIPAY_SALT, ALIPAY_ID, ALIPAY_EMAIL)

def _alipay_payurl(
        user_id, total_fee, return_url, notify_url, subject, buyer_email=None,
        for_id=0, body=''
    ):
    if buyer_email is None:
        buyer_email = mail_by_user_id(user_id)
    out_trade_no = charge_new(total_fee, user_id, CID_PAY_ALIPAY, for_id)
    return ALIPAY.payurl(
        total_fee,
        out_trade_no,
        subject,
        return_url,
        notify_url,
        buyer_email,
        body
    )


def alipay_cent_with_tax(cent):
    cent = int(cent)
    tax = CHARGE_TAX[CID_PAY_ALIPAY]
    return int((cent+1) / (1-tax))


def alipay_payurl_with_tax(
        user_id, yuan, return_url, notify_url, subject, buyer_email=None,
        for_id=0
    ):
    cent = int(float(yuan) * 100)
    total_fee = alipay_cent_with_tax(cent) / 100.0
    return _alipay_payurl(
        user_id,
        total_fee,
        return_url,
        notify_url,
        subject,
        buyer_email,
        for_id,
        '支付宝手续费 %.2f 元' % (total_fee - cent / 100.0)
    )


def alipay_payurl(
        user_id, total_fee, return_url, notify_url, subject, buyer_email=None,
        for_id=0
    ):
    total_fee = float(total_fee)
    return _alipay_payurl(
        user_id,
        total_fee,
        return_url,
        notify_url,
        subject,
        buyer_email,
        for_id,
        '%s'%buyer_email
    )

####
#def deal_new(price, from_id, to_id, rid, state=TRADE_STATE_ONWAY):
#   assert price > 0
#   cent = int(price * 100)
#   return trade_new(cent, 0, from_id, to_id, CID_TRADE_DEAL, rid, state)
#def alipay_payurl_pay(
#        from_user_id, to_user_id, total_fee, return_url, notify_url, subject, buyer_email
#    ):
#    cent = float(total_fee * 100)
#    tax = float(round(cent * CHARGE_TAX[CID_PAY_ALIPAY]))
#    after_tax = (cent-tax)/100
#    for_id = trade_id
#    out_trade_no = charge_new(total_fee, from_user_id, CID_PAY_ALIPAY, for_id)
#    body = '%s 捐赠> %s 跳转> %s' % (buyer_email, to_user_id, return_url)
#    return ALIPAY.payurl(
#        total_fee,
#        out_trade_no,
#        subject,
#        return_url,
#        notify_url,
#        buyer_email,
#        body,
#    )
#
#def alipay_payurl_with_tax(
#        user_id, total_fee, return_url, notify_url, subject, buyer_email=None
#    ):
#    total_fee = int(float(total_fee)*100)/100.
#    _total_fee = int(int(float(total_fee)*100+0.5)/ALIPAY_TAX)/100.
#    alipay_tax = _total_fee - total_fee
#    if alipay_tax:
#        subject += ' (支付宝手续费%s)' % alipay_tax
#    return _alipay_payurl(
#        user_id,
#        _total_fee,
#        return_url,
#        notify_url,
#        subject,
#        buyer_email
#    )

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
    return alipay_recall(d)

def alipay_recall(d):
    if d.get('trade_status') not in ('TRADE_FINISHED', 'TRADE_SUCCESS'):
        return

    result = ALIPAY.recall_valid(d)
    if not result:
        return False

    #如果验证有效 , 下面的参数肯定有
    trade_no = d['trade_no']
    out_trade_no = d['out_trade_no']
    total_fee = d['total_fee']
    return charged(out_trade_no, total_fee, CID_PAY_ALIPAY, d)
