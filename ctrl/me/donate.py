#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import LoginBase
#TEMP ZsiteBase
from ctrl.zsite._handler import ZsiteBase
from ctrl._urlmap.me import urlmap
from model.zsite import Zsite
from config import RPC_HTTP
from model.money_alipay import alipay_payurl, donate_alipay_payurl
from model.user_mail import mail_by_user_id, user_id_by_mail, user_mail_new
from model.money import bank_can_pay, bank_change, deal_new, TRADE_STATE_FINISH
from model.zsite import zsite_new, ZSITE_STATE_NO_PASSWORD, ZSITE_STATE_ACTIVE
from zkit.txt import EMAIL_VALID
from model.cid import CID_USER, CID_PAY_STATION

def check_account(alipay_account):
    error = None
    if not EMAIL_VALID.match(alipay_account):
        error = '请输入正确的支付宝邮箱'
    return alipay_account, error

def check_amount(amount):
    error = None
    try:
        amount = float(amount)
        amount_cent = amount * 100
        #amount = amount * 1.015
    except ValueError:
        error = '请输入金额数值'
    else:
        amount_min = 0.1
        amount_max = 100000000
        if amount < amount_min:
            error = '捐赠最少为%s' % amount_min
        elif amount > amount_max:
            error = '捐赠最多为%s' % amount_max
    return amount, error


@urlmap('/donate/result')
class Result(LoginBase):
    def get(self):
        self.render()

@urlmap('/donate/(\w+)')
class Index(ZsiteBase):

    def get(self, id):
        to_user_id = id
        to_user = Zsite.get(id=to_user_id)
        to_user_name = to_user.name
        no_login=False
        if not self.current_user:
            no_login=True
        self.render(
                alipay_account='',
                to_user_name=to_user_name,
                to_user_link=to_user.link,
                no_login=no_login,
                amount=0.42,
        )

    def post(self, id):
        NO_LOGIN = None
        to_user_id = int(id)
        to_user = Zsite.get(id=to_user_id)
        to_user_name = to_user.name
        amount = self.get_argument('amount', 0)
        if not self.current_user:
            alipay_account = self.get_argument('alipay_account', '')
        else:
            alipay_account = mail_by_user_id(self.current_user.id)
        amount, error = check_amount(amount)
        amount_cent = amount * 100

        #逻辑有些混乱
        if not error:
            if not self.current_user:
                # 通过current_user 判断是否为登陆状态
                alipay_account, error = check_account(alipay_account)
                from_user_id = user_id_by_mail(alipay_account)
                if from_user_id:
                    from_user = Zsite.get(id=from_user_id)
                    from_user_state = from_user.state
                    if from_user_state == ZSITE_STATE_ACTIVE:
                        #有激活账号但是没登录
                        NO_LOGIN = True
                elif not error:
                    #没激活账号也没登录
                    from_user = zsite_new(name=alipay_account, cid=CID_USER, state=ZSITE_STATE_NO_PASSWORD)
                    user_mail_new(from_user.id, alipay_account)
            else:
                from_user = self.current_user

        if not error:
            from_user_id = from_user.id
            from_user_mail = mail_by_user_id(from_user_id)
            import pdb; pdb.set_trace()

            if self.current_user and bank_can_pay(from_user_id, amount_cent):
                #如果zpage账户有余额
                deal_new(amount, from_user_id, to_user_id, rid=CID_PAY_STATION,state=TRADE_STATE_FINISH)
                return self.redirect('/donate/result')
            else:
                #跳转到支付宝链接
                return_url = '%s/money/alipay_sync' % RPC_HTTP
                notify_url = '%s/money/alipay_async' % RPC_HTTP
                alipay_url = donate_alipay_payurl(
                        from_user_id,
                        to_user_id,
                        amount,
                        return_url,
                        notify_url,
                        '%s 向 %s 捐赠' %(from_user.name, to_user_name),
                        from_user_mail,
                )
                if NO_LOGIN:
                    return self.redirect('/auth/login?next=' + alipay_url)

                return self.redirect(alipay_url)

        self.render(amount=amount,
                alipay_account=alipay_account,
                to_user_name=to_user_name,
                to_user_link=to_user.link,
                error=error,
        )
