# -*- coding: utf-8 -*-
from _handler import LoginBase
from ctrl._urlmap_istarsea.i import urlmap
from config import SITE_HTTP, RPC_HTTP
from model.cid import CID_TRADE_CHARDE, CID_PAY_ALIPAY
from model.money import bank, Trade, trade_history, pay_account_new, pay_account_name_get, withdraw_new, TRADE_STATE_FINISH
from model.money_alipay import alipay_payurl
from model.user_auth import user_password_verify
from model.zsite import Zsite
from zkit.errtip import Errtip

@urlmap('/money/pay')
class Pay(LoginBase):
    def get(self):
        return self.render()


@urlmap('/money/bill')
class Bill(LoginBase):
    def get(self):
        user_id = self.current_user_id
        trade_list = trade_history(user_id)


        user_ids = set([i.from_id if i.to_id == user_id else i.to_id for i in trade_list])
        if 0 in user_ids:
            user_ids.remove(0)
        user_dic = Zsite.mc_get_dict(list(user_ids))
        user_dic[user_id] = self.current_user
        user_dic[0] = None
        for t in trade_list:
            t.from_user = user_dic[t.from_id]
            t.to_user = user_dic[t.to_id]
        self.render(trade_list=trade_list)


@urlmap('/money/charge')
@urlmap('/money/charge/(\d{1,8}(?:\.\d{1,2})?)')
class Charge(LoginBase):
    def get(self, price='4.2'):
        self.render(price=price)

    def post(self, price=None):
        price = self.get_argument('price', None)
        error = None
        try:
            price = float(price)
        except ValueError:
            error = '金额输入错误'
        else:
            price_min = 0.05
            price_max = 100000000
            if price < price_min:
                error = '充值下限为 %s 元' % price_min
            elif price > price_max:
                error = '充值上限为 %s 元' % price_max
            else:
                return_url = '%s/money/alipay_sync' % SITE_HTTP
                notify_url = '%s/money/alipay_async' % RPC_HTTP
                return self.redirect(
                    alipay_payurl(
                        self.current_user_id,
                        price,
                        return_url,
                        notify_url,
                        '%s 充值' % self.current_user.name,
                    )
                )

        self.render(
            price=price,
            error=error,
        )




@urlmap('/money/draw')
class Draw(LoginBase):
    def get(self):
        user_id = self.current_user_id
        account, name = pay_account_name_get(user_id, CID_PAY_ALIPAY)
        self.render(
            account=account,
            name=name,
        )

    def post(self):
        user_id = self.current_user_id
        password = self.get_argument('password', '')
        account = self.get_argument('account', '')
        name = self.get_argument('name', '')
        price = self.get_argument('price', '')

        if user_password_verify(user_id, password):
            a = pay_account_new(user_id, account, name, CID_PAY_ALIPAY)
            try:
                price = float(price)
            except ValueError:
                error = '金额输入错误'
            else:
                price_min = 0.05
                price_max = bank.get(user_id) / 100.

                if price > price_max:
                    error = '提现超出余额'
                elif price < price_min:
                    error = '提现下限为 %s 元' % price_min
                else:
                    t = withdraw_new(price, user_id, CID_PAY_ALIPAY)
                    return self.redirect('/money/drawed/%s' % t.id)
        else:
            error = '密码有误'

        self.render(
            price=price,
            account=account,
            name=name,
            error=error,
        )

@urlmap('/money/charged/(\d+)')
@urlmap('/money/charged/(\d+)/(\d+)')
class Charged(LoginBase):
    def get(self, tid, uid=0):
        uid = int(uid)
        t = Trade.get(tid)
        return self.render(trade=t)
        if t and t.cid == CID_TRADE_CHARDE and t.state == TRADE_STATE_FINISH and t.to_id == uid:
            self.render(trade=t)
        else:
            self.redirect('/money')

@urlmap('/money/drawed/(\d+)')
class Drawed(LoginBase):
    def get(self, tid):
        t = Trade.get(tid)
        if t and t.from_id == self.current_user_id:
            self.render(trade=t)
        else:
            self.redirect('/money/bill')
