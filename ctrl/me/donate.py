#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import LoginBase
from ctrl._urlmap.me import urlmap
from model.zsite import Zsite
from config import RPC_HTTP
from model.money_alipay import alipay_payurl

@urlmap('/donate/(\w+)')
class Index(LoginBase):
    def get(self, id):
        by_donar_id = id
        by_donar = Zsite.get(id=by_donar_id)
        by_donar_name = by_donar.name
        self.render(by_donar_name=by_donar_name,
                    by_donar_link=by_donar.link,
                    amount=0.42,
        )
    
    def post(self, id):
        by_donar_id = id
        by_donar = Zsite.get(id=by_donar_id)
        by_donar_name = by_donar.name
        donar_id = self.current_user_id

        amount = self.get_argument('amount', 0) 
####
        error = None
        try:
            amount = float(amount)
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
                    alipay_payurl(
                        by_donar_id,
                        amount,
                        return_url,
                        notify_url,
                        '%s 捐赠' % self.current_user.name,
                        self.current_user.name,
                    )
                )

        self.render(amount=amount,
                    by_donar_name=by_donar_name,
                    by_donar_link=user.link,
                    error=error,
        )

        


##@urlmap('/donate')
#def Index(LoginBase):
#    def get(self):
#        user_id = self.current_user_id
#        user = Zsite.get(id=user_id)
#        user_name = user.name
#        self.render(user_name=usr_name)
#        
