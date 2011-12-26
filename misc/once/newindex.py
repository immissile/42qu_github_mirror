#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from model.zsite_list import ZsiteList
from model.zsite import Zsite
from model.buzz import Buzz
from model.kv_misc import kv_int
CID_BUZZ_SHOW = 212
for i in Buzz.where(cid=CID_BUZZ_SHOW):
    i.delete()
    print "delete buzz show", i.id

    KV_SHOW_BUZZ_POS = 1 # 加入Show的非重要通知
    kv_int.delete(KV_SHOW_BUZZ_POS)
