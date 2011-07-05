#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import LoginBase
#TEMP ZsiteBase
from ctrl.zsite._handler import ZsiteBase
from ctrl._urlmap.me import urlmap
from model.zsite import Zsite
from config import RPC_HTTP
from model.money_alipay import alipay_payurl, donate_alipay_payurl
from model.user_mail import mail_by_user_id
from model.money import bank_can_pay, bank_change
from model.zsite import zsite_new, ZSITE_STATE_NO_PASSWORD
from zkit.txt import EMAIL_VALID
from model.cid import CID_USER

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
        self.render(to_user_name=to_user_name,
                    to_user_link=to_user.link,
                    no_login=no_login,
                    amount=0.42,
        )
    
    def post(self, id):
        to_user_id = id
        to_user = Zsite.get(id=to_user_id)
        to_user_name = to_user.name
        amount = self.get_argument('amount', 0) 
        amount, error = check_amount(amount)  
        from_user = None

        #逻辑有些混乱
        #有账号但是没登陆
        NO_LOGIN = False
        import pdb;pdb.set_trace()
        if not self.current_user and not error:
            alipay_account = self.get_argument('alipay_account', '')
            alipay_account, error = check_amount(alipay_account)
            # 通过current_user 判断是否为登陆状态
            from_user_id = user_id_by_mail(alipay_account)
            if from_user_id:
                NO_LOGIN = True
                from_user = Zsite
                #login,alipay
                
            else:
                from_user = zsite_new(name=alipay_account, cid=CID_USER, state=ZSITE_STATE_NO_PASSWORD)
        if not from_user:
            from_user = self.current_user
            from_user_id = from_user.id
            from_user_mail = mail_by_user_id(from_user_id)

        if not error:
            if bank_can_pay(from_user_id, amount_cent):
                bank_change(from_user_id, -amount_cent)
                bank_change(to_user_id, amount_cent)
                url = "/donate/result"
                return self.redirect(url)
            else:
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
                    return self.redirect('/auth/login?next='+alipay_url)

                return self.redirect(alipay_url)

            self.render(amount=amount,
                    to_user_name=to_user_name,
                    to_user_link=to_user.link,
                    error=error,
            )

def check_amount(alipay_account):
    error = None
    if not EMAIL_VALID.match(mail):
        error = '邮箱格式错误'
    return alipay_account, error

def check_amount(amount):
    error = None
    try:
        amount = float(amount)
        amount_cent = amount * 100
        #amount = amount * 1.015
    except ValueError:
        error = '金额输入错误'
    else:
        amount_min = 0.1
        amount_max = 100000000
        if amount < amount_min:
            error = '捐赠最少为%s' % amount_min
        elif amount > amount_max:
            error = '捐赠最多为%s' % amount_max
        else:
            return amount, error
       
