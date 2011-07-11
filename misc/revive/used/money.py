#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from qu.mysite.model.money import bank_price_by_man_id, pay_onway_from_total, pay_onway_to_total, draw_account_get

from zpage.model.zsite import Zsite
from zpage.model.money import bank

def init_bank():
    for zsite_id in Zsite.where().col_list():
        b0 = bank_price_by_man_id(zsite_id)
        b1 = pay_onway_from_total(zsite_id)
        b2 = pay_onway_to_total(zsite_id)
        if b0 or b1:
            b = int(100 * (float(b0) + float(b1)))
            bank.set(zsite_id, b)


if __name__ == '__main__':
    init_bank()
