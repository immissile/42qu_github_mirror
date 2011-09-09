#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kv import Kv

kv_int = Kv('kv_int', 0)
kv_txt = Kv('kv_txt')


def kv_int_call(key, f):
    '''
    def f(old):
        return new
    '''
    old = kv_int.get(key)
    new = f(old)
    if new:
        kv_int.set(key, new)
    return new

# Key
KV_SHOW_BUZZ_POS = 1 # 加入Show的非重要通知
KV_NOTICE_POS = 2 # 重要通知邮件
KV_ZSITE_RANK_POWER = 3 # 排序的基数
KV_BUZZ_SYS_POS = 4 # 全站buzz通知
KV_BUZZ_FOLLOW_POS = 5 # follow邮件通知
KV_OAUTH_FOLLOW = 6 # 用户微博关注官方微博
KV_PO_AUDIO = 7 # 音频压缩
KV_EVENT_STATE = 8 # 活动开始与结束
KV_EVENT_READY = 9 # 活动后天开始提醒
KV_EVENT_WEEK = 10 # 活动周报位置
KV_EVENT_PAY = 11 # 活动结束转账
KV_SEO_PING = 12 # SEO ping PO

#微博同步
KV_SYNC_PO_BY_ZSITE_ID = 15 # 发文 
KV_SYNC_JOIN_EVENT_BY_ZSITE_ID = 16 # 参加活动
KV_SYNC_RECOMMEND_BY_ZSITE_ID = 17 # 分享文章 


