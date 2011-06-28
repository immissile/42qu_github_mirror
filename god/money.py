#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.money import withdraw_list, Trade, withdraw_fail, pay_account_get
from model.mail import sendmail, rendermail
from model.user_mail import mail_by_user_id


@urlmap('/withdraw')
class WithDraw(Base):
    def get(self):
        self.render( withdraw_list = withdraw_list())

    def post(self):
        id = self.get_argument('id','').strip()
        body = self.request.body
        if "reject=" in body:
            i = Trade.get(id)
            cid = i.cid
            i.account, i.name = pay_account_get(i.from_id, i.rid)
            txt = "%s 提现失败"%cid   
            withdraw_fail(id,txt)
            mail = mail_by_user_id(id)
            rendermail('/mail/notice/with_draw.txt',mail,i.name,cid = i.cid, name = i.name,account = i.account, value = i.value/100.0))
            return self.get()
        else:
            trade_no = self.get_argument('trade_no','').strip()
            if trade_no:
                trade = Trade.get(id)
                trade.finish()
                return self.get()

