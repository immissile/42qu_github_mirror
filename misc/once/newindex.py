#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from model.zsite_list import ZsiteList
from zweb.orm import ormiter
from model.zsite import Zsite
from model.buzz import Buzz
from model.kv_misc import kv_int
from model.cid import CID_BUZZ_FOLLOW , CID_BUZZ_EVENT_JOIN , CID_BUZZ_SITE_NEW , CID_BUZZ_SITE_FAV , CID_BUZZ_PO_REPLY , CID_BUZZ_SYS , CID_BUZZ_EVENT_FEEDBACK_JOINER , CID_BUZZ_EVENT_FEEDBACK_OWNER  

cid_set = (CID_BUZZ_FOLLOW , 
CID_BUZZ_EVENT_JOIN , 
CID_BUZZ_SITE_NEW , 
CID_BUZZ_SITE_FAV , 

CID_BUZZ_PO_REPLY , 

CID_BUZZ_SYS , 
CID_BUZZ_EVENT_FEEDBACK_JOINER , 
CID_BUZZ_EVENT_FEEDBACK_OWNER  , 
)
 

for i in ormiter(Buzz):
    if i.cid not in cid_set:
        i.delete()
        print i.id
KV_SHOW_BUZZ_POS = 1 # 加入Show的非重要通知
kv_int.delete(KV_SHOW_BUZZ_POS)


