#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib import quote_plus, unquote
from urlparse import parse_qsl
from hashlib import md5

ALIPAY_DEFALUT_PAY_PARAM = dict(
    service='create_direct_pay_by_user', #即时到帐接口
    _input_charset='utf-8',
    payment_type='1',
    paymethod='bankPay',
)

def alipay_sign(salt, param):
    param.sort(key=lambda x:x[0])

    result = []
    for k, v in param:
        v = str(v)
        #v = quote(v)
        if v:
            result.append("%s=%s"%(k, v))
    param = "&".join(result)
    return md5(param+salt).hexdigest()

def alipay_url_parse(url):
    url = url.split("?", 1)[-1]
    r = parse_qsl(url)
    return r

def alipay_recall_valid(salt, d):
    sign = None
    r = []
    for k, v in  sorted(d):
        if k == "sign":
            sign = v
        elif k == "sign_type":
            pass
        elif v:
            r.append((k, v))
    return alipay_sign(salt, r) == sign

class Alipay(object):
    def __init__(self, salt, seller_id, seller_email):
        self.salt = salt
        self.param = param = ALIPAY_DEFALUT_PAY_PARAM.copy()
        self.seller_id = param['partner'] = seller_id
        self.seller_email = param['seller_email'] = seller_email

    def payurl(
            self,
            total_fee,
            out_trade_no,
            subject,
            return_url,
            notify_url,
            buyer_email,
            body=''
        ):
        param = self.param.copy()
        param['total_fee'] = total_fee
        param['out_trade_no'] = out_trade_no
        param['subject'] = subject
        param['return_url'] = return_url
        param['notify_url'] = notify_url
        if body:
            param['body'] = body
        #param['show_url'] = show_url
        if buyer_email != self.seller_email:
            param['buyer_email'] = buyer_email
        sign = alipay_sign(self.salt, param.items())

        url = 'https://www.alipay.com/cooperate/gateway.do?%s&sign=%s&sign_type=MD5'%(
            "&".join("%s=%s"%(k, quote_plus(str(v))) for k, v in param.iteritems()),
            sign
        )
        return url

    def recall_valid(self, d):
        if d.get('seller_id') != self.seller_id:
            return
        if d.get('seller_email') != self.seller_email:
            return
        vaild = alipay_recall_valid(self.salt, d.items())
        return vaild

######################### 支付宝 #########################
from config import ALIPAY_ID, ALIPAY_SALT, ALIPAY_EMAIL
ALIPAY = Alipay(ALIPAY_SALT, ALIPAY_ID, ALIPAY_EMAIL)

def _alipay_payurl(
        man_id, total_fee, return_url, notify_url, subject, buyer_email=None
    ):
    if buyer_email is None:
        buyer_email = man_mail_get(man_id) or ''
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
