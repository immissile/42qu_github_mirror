#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model
from zsite import Zsite
from po import Po
import time

LOG_HISTORY_NEW_USER_CID = 1
LOG_HISTORY_NEW_PO_CID = 2
LOG_HISTORY_NEW_PO_USER_CID = 3

class LogHistory(Model):
    pass


def int2date(day):
    return date.fromtimestamp(day*3600*24)

def today_int():
    return int((8+time.time()/3600)/24)

def log_new_user():
    num_today = Zsite.raw_sql('select count(1) from zsite').fetchone()[0]
    today = today_int()
    num_pre = LogHistory.where(day = today-1,cid = LOG_HISTORY_NEW_USER_CID ).col_list(col =' num')
    if num_pre:
        LogHistory.raw_sql('insert into log_history (day, num, incr,cid) values(%s,%s,%s,%s)',today,num_today,num_today-num_pre,LOG_HISTORY_NEW_USER_CID)
    else:
        LogHistory.raw_sql('insert into log_history (day,num,incr,cid) values(%s,%s,%s,%s)',today,num_today,0,LOG_HISTORY_NEW_USER_CID)

def log_new_po():
    num_today = Po.raw_sql('select count(1) from po').fetchone()[0]
    print num_today
    today = today_int()
    num_pre = LogHistory.where(day = today-1,cid = LOG_HISTORY_NEW_PO_CID).col_list(col='num')
    print num_pre
    if num_pre:
        LogHistory.raw_sql('insert into log_history (day,num,incr,cid) values(%s,%s,%s,%s)',today,num_today,num_today-num_pre,LOG_HISTORY_NEW_PO_CID)
    else:
        LogHistory.raw_sql('insert into log_history (day,num,incr,cid) values(%s,%s,%s,%s)',today,num_today,0,LOG_HISTORY_NEW_PO_CID)

def log_new_po_user():
    po_peo = Po.raw_sql('select count(distinct(user_id)) from po').fetchone()[0]
    pass
if __name__ == '__main__':
    print log_new_po()


