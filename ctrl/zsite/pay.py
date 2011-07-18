#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import ZsiteBase, LoginBase
from zkit.errtip import Errtip
from ctrl._urlmap.zsite import urlmap
from model.zsite import Zsite
from config import RPC_HTTP, SITE_DOMAIN
from model.money_alipay import alipay_payurl, alipay_payurl_with_tax
from model.user_mail import mail_by_user_id, user_by_mail
from model.money import bank_can_pay, bank_change, pay_new, deal_new, TRADE_STATE_NEW, TRADE_STATE_ONWAY, TRADE_STATE_FINISH, pay_account_get, bank_view, Trade, trade_log, pay_notice
from model.zsite import zsite_new, ZSITE_STATE_NO_PASSWORD, ZSITE_STATE_ACTIVE, ZSITE_STATE_APPLY
from zkit.txt import EMAIL_VALID
from model.cid import CID_USER, CID_PAY_ALIPAY, CID_TRADE_PAY
from model.user_auth import user_new_by_mail
from yajl import dumps, loads
from model.state import STATE_SECRET, STATE_ACTIVE
from model.notice import notice_new


@urlmap('/pay/result/(\d+)')
class Result(ZsiteBase):
    def get(self, id):
        t = Trade.get(id)
        from_user = Zsite.mc_get(t.from_id)
        to_user = Zsite.mc_get(t.to_id)

        self.render(
            from_user=from_user,
            to_user=to_user,
            trade=t,
        )

@urlmap('/pay')
class Index(ZsiteBase):

    NOTIFY_URL = '%s/money/alipay_async/%%s' % RPC_HTTP

    def _arguments(self):
        url = self.get_argument('url', '')
        title = self.get_argument('title', '')
        return url, title

    def get(self):
        current_user = self.current_user
        current_user_id = self.current_user_id
        url, title = self._arguments()
        price = self.get_argument('price', 4.2)

        if current_user:
            alipay_account = pay_account_get(
                current_user_id,
                CID_PAY_ALIPAY
            )
        else:
            alipay_account = ''

        self.render(
            url=url,
            title=title,
            amount=price,
            errtip=Errtip(),
            alipay_account=alipay_account
        )

    def post(self):
        current_user = self.current_user
        zsite = self.zsite
        request = self.request
        errtip = Errtip()
        zsite_id = self.zsite_id

        url, title = self._arguments()
        amount = self.get_argument('amount', 0)
        alipay_account = self.get_argument('alipay_account', '')

        if not amount:
            errtip.amount = '请输入金额'
        else:
            try:
                amount = float(amount)
            except ValueError:
                errtip.amount = '%s 不是有效的金额'%amount
            else:
                if amount <= 0:
                    errtip.amount = '金额须大于零'
                elif amount >= 9999999:
                    errtip.amount = '金额超出上限'
                else:
                    amount_cent = amount * 100

        if not current_user:
            mail = self.get_argument('mail', '')
            if not mail:
                errtip.mail = '请输入联系邮箱'
            elif not EMAIL_VALID.match(mail):
                errtip.mail = '邮箱无效'
            else:
                user = user_by_mail(mail)
                self.set_cookie('E', mail.strip().lower())
                if not user:
                    user = user_new_by_mail(mail)
                elif user.state >= ZSITE_STATE_APPLY:
                    return self.redirect(
                              '/auth/login?next=%s'%request.uri
                           )
                current_user = user

        if current_user and not errtip:
            subject = '%s 向 %s 捐赠 %.2f 元' % (current_user.name, zsite.name, amount)
            current_user_id = current_user.id
            _pay_new = lambda state : pay_new(amount, current_user_id, zsite_id, CID_TRADE_PAY, state)
            balance_cent = float(bank_view(current_user_id)) * 100



            txt = self.get_argument('txt', None)
            secret = self.get_argument('secret', None)

            message = {}

            if title:
                message['title'] = title
            if url:
                message['url'] = url
            if txt:
                message['txt'] = txt
                if secret:
                    message['secret'] = secret




            if balance_cent >= amount_cent:
                o_id = _pay_new(TRADE_STATE_FINISH)
                if message:
                    trade_log.set(o_id, dumps(message))
                pay_notice(o_id)

                return self.redirect('/pay/result/%s'%o_id)
            elif balance_cent > 0:
                subject += '(余额支付 %.2f 元)' % (balance_cent/100.0)
                o_id = _pay_new(TRADE_STATE_NEW)
                amount_cent -= balance_cent
            else:
                o_id = _pay_new(TRADE_STATE_NEW)

            trade_log.set(o_id, dumps(message))

            return_url = 'http://%s/money/alipay_sync' % SITE_DOMAIN

            alipay_url = alipay_payurl_with_tax(
                    current_user_id,
                    amount_cent/100.0,
                    self.NOTIFY_URL,
                    subject,
                    alipay_account,
                    o_id
            )

            return self.redirect(alipay_url)

        self.render(
            url=url, title=title,
            amount=amount,
            errtip=errtip,
            alipay_account=alipay_account
        )

