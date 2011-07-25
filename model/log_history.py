#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model
from zsite import Zsite
from po import Po
from reply import Reply
import time

LOG_HISTORY_NEW_USER_CID = 1
LOG_HISTORY_NEW_PO_CID = 2
LOG_HISTORY_NEW_PO_USER_CID = 3
LOG_HISTORY_NEW_REPLY_CID = 4

class LogHistory(Model):
    pass

def int2date(day):
    return date.fromtimestamp(day*3600*24)

def today_int():
    return int((8+time.time()/3600)/24)

def fa2l(t): #tupe by fetchall() 2 list
    n = ()
    for i in t:
        n += i
    return n

def log_update(cid, limit=100):
    n = LogHistory.raw_sql('select incr from log_history where cid = %s limit %s',cid, limit).fetchall()
    num = fa2l(n)
    return num
    
def log_new_user():
    num_today = Zsite.raw_sql('select count(1) from zsite').fetchone()[0]
    today = today_int()
    num_pre = LogHistory.where(day=today-1, cid=LOG_HISTORY_NEW_USER_CID ).col_list(col=' num')
    if num_pre:
        LogHistory.raw_sql('insert into log_history (day, num, incr,cid) values(%s,%s,%s,%s)', today, num_today, num_today-num_pre, LOG_HISTORY_NEW_USER_CID)
    else:
        LogHistory.raw_sql('insert into log_history (day,num,incr,cid) values(%s,%s,%s,%s)', today, num_today, 0, LOG_HISTORY_NEW_USER_CID)

def log_new_po():
    num_today = Po.raw_sql('select count(1) from po').fetchone()[0]
    today = today_int()
    num_pre = LogHistory.where(day=today-1, cid=LOG_HISTORY_NEW_PO_CID).col_list(col='num')
    if num_pre:
        LogHistory.raw_sql('insert into log_history (day,num,incr,cid) values(%s,%s,%s,%s)', today, num_today, num_today-num_pre, LOG_HISTORY_NEW_PO_CID)
    else:
        LogHistory.raw_sql('insert into log_history (day,num,incr,cid) values(%s,%s,%s,%s)', today, num_today, 0, LOG_HISTORY_NEW_PO_CID)

def log_new_po_user():
    num_today = Po.raw_sql('select count(distinct(user_id)) from po').fetchone()[0]
    today = today_int()
    num_pre = LogHistory.where(day=today-1, cid=LOG_HISTORY_NEW_USER_CID).col_list(col='num')[:1]
    if num_pre:
        LogHistory.raw_sql('insert into log_history (day,num,incr,cid) values(%s,%s,%s,%s)', today, num_today, num_today-num_pre[0], LOG_HISTORY_NEW_PO_USER_CID)
    else:
        LogHistory.raw_sql('insert into log_history (day,num,incr,cid) values(%s,%s,%s,%s)', today, num_today, 0, LOG_HISTORY_NEW_PO_USER_CID)

def log_new_reply():
    num_today = Reply.raw_sql('select count(1) from reply').fetchone()[0]
    today = today_int()
    num_pre = LogHistory.where(day=today-1, cid=LOG_HISTORY_NEW_REPLY_CID).col_list(col='num')[:1]
    print num_pre
    if num_pre:
        LogHistory.raw_sql('insert into log_history (day,num,incr,cid) values(%s,%s,%s,%s)', today, num_today, num_today-num_pre[0], LOG_HISTORY_NEW_REPLY_CID)
    else:
        LogHistory.raw_sql('insert into log_history (day,num,incr,cid) values(%s,%s,%s,%s)', today, num_today, 0, LOG_HISTORY_NEW_REPLY_CID)

def all_incr():    #返回所有的增长数
    user, po, pouser, reply = log_update(LOG_HISTORY_NEW_USER_CID),log_update(LOG_HISTORY_NEW_PO_CID),\
                              log_update(LOG_HISTORY_NEW_PO_USER_CID),log_update(LOG_HISTORY_NEW_REPLY_CID)
    return user,po,pouser,reply

def today_all_num():     #返回所有的今天数据
    num_user = LogHistory.raw_sql("select incr from log_history where cid = %s order by day desc", LOG_HISTORY_NEW_USER_CID).fetchone()[0]
    num_po = LogHistory.raw_sql("select incr from log_history where cid = %s order by day desc", LOG_HISTORY_NEW_PO_CID).fetchone()[0]
    num_po_user = LogHistory.raw_sql("select incr from log_history where cid = %s order by day desc", LOG_HISTORY_NEW_PO_USER_CID).fetchone()[0]
    num_reply = LogHistory.raw_sql("select incr from log_history where cid = %s order by day desc", LOG_HISTORY_NEW_REPLY_CID).fetchone()[0]
    return num_user, num_po, num_po_user, num_reply

def log_new(): #更新每天的数据
    log_new_user()
    log_new_po()
    log_new_po_user()
    log_new_reply()

if __name__ == '__main__':
    log_new()
