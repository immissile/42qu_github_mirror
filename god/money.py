#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.money import withdraw_list, Trade, withdraw_fail, pay_account_name_get, withdraw_success
from model.mail import rendermail

CID2CN = {
    152: '支付宝'
}

@urlmap('/withdraw')
class WithDraw(Base):
    def get(self):
        self.render(withdraw_list=withdraw_list())

    def post(self):
        id = self.get_argument('id', '').strip()
        i = Trade.get(id)
        if not i:
            return
        body = self.request.body
        if 'reject=' in body:
            cid = i.cid
            i.account, i.name = pay_account_name_get(i.from_id, i.rid)
            txt = '%s 提现失败'%CID2CN[int(cid)]
            withdraw_fail(id, txt)
        else:
            trade_no = self.get_argument('trade_no', '').strip()
            if trade_no:
                withdraw_success(id, trade_no)
        return self.redirect('/withdraw')
