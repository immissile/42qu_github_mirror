#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from zweb._urlmap import urlmap
from config import SITE_HTTP
#from model.money import *
from zkit.txt import EMAIL_VALID, mail2link
from model.cid import CID_VERIFY_MAIL, CID_VERIFY_PASSWORD
from model.user_auth import user_password_new
from model.user_mail import mail_by_user_id, user_id_by_mail
from model.verify import verify_new, verify
from model.zsite import Zsite, ZSITE_STATE_APPLY, ZSITE_STATE_ACTIVE
from model.user_session import user_session

@urlmap('/money')
class Money(LoginBase):
    def get(self):
        pass

@urlmap('/money/charge')
@urlmap('/money/charge/(\d{1,8}(?:\.\d{1,2})?)')
class Charge(LoginBase):
    def get(self, price='42'):
        return self.finish(price)
        self.render(price=price)

    def post(self, price=None):
        price = self.get_argument('price', None)
        error = None
        try:
            price = float(price)
        except ValueError:
            error = '金额输入错误'
        else:
            charge_min = 0.42
            charge_max = 100000000
            if price < charge_min:
                error = '单笔充值最少为%s' % charge_min
            elif price > charge_max:
                error = '单笔充值最多为%s' % charge_max
            else:
                return_url = '%s/rpc/money/alipay_sync' % SITE_HTTP
                notify_url = '%s/rpc/money/alipay_async' % SITE_HTTP
                return self.redirect(
                    alipay_charge(
                        self.current_user_id,
                        price,
                        return_url,
                        notify_url,
                        '%s充值' % self.current_user.name,
                    )
                )

@urlmap('/money/draw')
class Draw(LoginBase):
    def get(self):
        pass

    def post(self):
        pass
