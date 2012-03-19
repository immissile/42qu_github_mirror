#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib import quote_plus
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
            result.append('%s=%s'%(k, v))
    param = '&'.join(result)
    return md5(param+salt).hexdigest()

def alipay_url_parse(url):
    qs = url.split('?', 1)[-1]
    t = parse_qsl(qs)
    return dict(t)

def alipay_recall_valid(salt, d):
    sign = None
    r = []
    for k, v in sorted(d):
        if k == 'sign':
            sign = v
        elif k == 'sign_type':
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

        url = 'https://www.alipay.com/cooperate/gateway.do?%s&sign=%s&sign_type=MD5' % (
            '&'.join('%s=%s' % (k, quote_plus(str(v))) for k, v in param.iteritems()),
            sign
        )
        return url

    def recall_valid(self, d):
        if d.get('seller_id') != self.seller_id:
            return
        if d.get('seller_email') != self.seller_email:
            return
        return alipay_recall_valid(self.salt, d.items())
