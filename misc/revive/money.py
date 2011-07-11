#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from qu.mysite.model.money import bank_price_by_man_id, pay_onway_from_total, pay_onway_to_total, draw_account_get

from zpage.model.zsite import Zsite
from zpage.model.money import

def bank():
    for zsite_id in Zsite.where().col_list():
        print zsite_id
        print bank_price_by_man_id(zsite_id)
        print pay_onway_from_total(zsite_id)
        print pay_onway_to_total(zsite_id)
