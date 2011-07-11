#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from qu.mysite.model.money import DrawAccount, draw_account_get, CID_BANK_ALIPAY

from zpage.model.zsite import Zsite
from zpage.model.money import bank, pay_account_new, CID_PAY_ALIPAY

def init_acc():
    for zsite_id in Zsite.where().col_list():
        a = DrawAccount.get(man_id=zsite_id, cid=CID_BANK_ALIPAY)
        if a:
            name = a.name
            account = a.account
            pay_account_new(zsite_id, account, name, CID_PAY_ALIPAY)


if __name__ == '__main__':
    init_acc()
