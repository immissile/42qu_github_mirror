#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import LoginBase
from ctrl._urlmap.me import urlmap
from model.zsite import Zsite
from config import RPC_HTTP
from model.money_alipay import alipay_payurl, donate_alipay_payurl
from model.user_mail import mail_by_user_id

@urlmap('/donate/(\w+)')
class Index(LoginBase):
    def get(self, id):
        to_user_id = id
        to_user = Zsite.get(id=to_user_id)
        to_user_name = to_user.name
        self.render(to_user_name=to_user_name,
                    to_user_link=to_user.link,
                    amount=0.42,
        )
    
    def post(self, id):
        to_user_id = id
        to_user = Zsite.get(id=to_user_id)
        to_user_name = to_user.name
        from_user = self.current_user
        from_user_mail = mail_by_user_id(from_user.id)

        amount = self.get_argument('amount', 0) 
        error = None
        try:
            amount = float(amount)
            amount = amount*1.015
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
                return_url = '%s/money/alipay_sync' % RPC_HTTP
                notify_url = '%s/money/alipay_async' % RPC_HTTP
                return self.redirect(
                    donate_alipay_payurl(
                        from_user.id,
                        to_user_id,
                        amount,
                        return_url,
                        notify_url,
                        '%s 向 %s 捐赠' %(from_user.name, to_user_name),
                        from_user_mail,
                    )
                )

        self.render(amount=amount,
                    to_user_name=to_user_name,
                    to_user_link=to_user.link,
                    error=error,
        )
        
