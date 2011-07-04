#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kv import Kv

kv_int = Kv('kv_int', 0)
kv_txt = Kv('kv_txt')

# Key
KV_SHOW_BUZZ_POS = 1 # 加入Show的非重要通知
KV_NOTICE_POS = 2 # 重要通知
KV_ZSITE_RANK_DAYS = 3 # rank统计到的天数
KV_ZSITE_RANK_POWER = 4 # 排序的基数
