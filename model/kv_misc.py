#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kv import Kv

kv_int = Kv('kv_int', 0)
kv_txt = Kv('kv_txt')

# Key
KV_SHOW_BUZZ_POS = 1 # 加入Show的非重要通知
KV_NOTICE_POS = 2 # 重要通知邮件
KV_ZSITE_RANK_POWER = 3 # 排序的基数
KV_BUZZ_SYS_POS = 4 # 全站buzz通知
KV_BUZZ_FOLLOW_POS = 5 # follow邮件通知
KV_OAUTH_FOLLOW = 6 #用户微博关注官方微博
