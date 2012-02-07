#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model
from zsite import Zsite
from po import Po
from reply import Reply
from model.days import today_days
import time
from model.cid import CID_USER
from operator import itemgetter
from follow import Follow
from model.privilege import PRIVILEGE_IMPORT_FEED
from model.part_time_job import PartTimeJob
from model.privilege import PRIVILEGE_CN


LOG_HISTORY_CID_USER = 1
LOG_HISTORY_CID_PO = 2
LOG_HISTORY_CID_REPLY = 3
LOG_HISTORY_CID_FOLLOW = 4
LOG_HISTORY_CID_PO_ZSITE = 5
LOG_HISTORY_CID_PRIVILEGE_IMPORT_FEED = 6

LOG_HISTORY_CID = (
    LOG_HISTORY_CID_USER,
    LOG_HISTORY_CID_PO,
    LOG_HISTORY_CID_REPLY,
    LOG_HISTORY_CID_FOLLOW,
    LOG_HISTORY_CID_PO_ZSITE,
    LOG_HISTORY_CID_PRIVILEGE_IMPORT_FEED
)
LOG_HISTORY_CN_CID = {
    LOG_HISTORY_CID_USER: '用户',
    LOG_HISTORY_CID_PO: '帖子',
    LOG_HISTORY_CID_REPLY: '回复',
    LOG_HISTORY_CID_FOLLOW:'关注',
    LOG_HISTORY_CID_PO_ZSITE:'小站贴',
    LOG_HISTORY_CID_PRIVILEGE_IMPORT_FEED:PRIVILEGE_CN[PRIVILEGE_IMPORT_FEED],
}

LOG_PART_TIME_MAPPING = {
    PRIVILEGE_IMPORT_FEED:LOG_HISTORY_CID_PRIVILEGE_IMPORT_FEED,
    }


#max_id = max(LOG_HISTORY_CID)
#PART_TIME_JOB_DICT = dict()
#for user_id,rule_list in PART_TIME_JOBS_RULES:
#    for rule in rule_list:
#        max_id += 1
#        PART_TIME_JOB_DICT[user_id,max_id]= ('%s - %s'%(Zsite.mc_get(user_id).name, PRIVILEGE_CN.get(rule)),rule)
#
#LOG_HISTORY_CN_CID.update([(cid,v[0]) for (user_id,cid),v in PART_TIME_JOB_DICT.items()])
#LOG_HISTORY_CID+=tuple([cid for (user_id,cid) in PART_TIME_JOB_DICT.keys()])


class LogHistory(Model):
    pass

def log_history_new(cls , cid, num, user_id=0, day=None):
    if day is None:
        day = today_days()
    c = LogHistory.raw_sql(
        'select num from log_history where cid=%s and day<%s order by day desc limit 1',
        cid, day
    )
    pre_num = c.fetchone()
    if pre_num:
        pre_num = pre_num[0]

    if pre_num:
        incr = num - pre_num
    else:
        incr = 0

    max_id = cls.raw_sql('select max(id) from %s'%cls.Meta.table).fetchone()
    if max_id:
        max_id = max_id[0]
    else:
        max_id = 0

    #print "'insert into log_history (day,num,incr,cid, max_id, user_id) values (%s,%s,%s,%s,%s,%s) on duplicate key update num=%s, incr=%s, max_id=%s'"%(day , num, incr, cid, max_id,user_id, num, incr, max_id)
    LogHistory.raw_sql(
'insert into log_history (day,num,incr,cid, max_id, user_id) values (%s,%s,%s,%s,%s,%s) on duplicate key update num=%s, incr=%s, max_id=%s',
    day , num, incr, cid, max_id, user_id, num, incr, max_id
    )


def log_incr_list(cid, limit=100):
    c = LogHistory.raw_sql(
'select incr, user_id from log_history where cid=%s order by day asc limit %s', cid, limit+1
    ).fetchall()
    user_id = c[0][1] if len(c) else 0
    return list(map(itemgetter(0), c))[1:], user_id


def log_part_time():
    from config import PRIVILEGE_ADMIN
    for user_id, v in PRIVILEGE_ADMIN:
        for part_time_cid in v:
            cid = LOG_PART_TIME_MAPPING[part_time_cid]
            num = PartTimeJob.raw_sql(
                'select count(1) from part_time_job where user_id=%s and cid=%s', user_id, part_time_cid
            ).fetchone()[0]
            #print cid,user_id,num
            log_history_new(PartTimeJob, cid, num, user_id=user_id)

def log_num_user():
    num = Zsite.raw_sql(
        'select count(1) from zsite where cid=%s', CID_USER
    ).fetchone()[0]
    log_history_new(Zsite, LOG_HISTORY_CID_USER, num)

def log_num_po():
    num = Po.raw_sql('select count(1) from po where zsite_id = 0').fetchone()[0]
    log_history_new(Po, LOG_HISTORY_CID_PO, num)


def log_num_po_zsite():
    num = Po.raw_sql('select count(1) from po where zsite_id != user_id').fetchone()[0]
    log_history_new(Po, LOG_HISTORY_CID_PO_ZSITE, num )


def log_num_reply():
    num = Reply.raw_sql('select count(1) from reply').fetchone()[0]
    log_history_new(Reply, LOG_HISTORY_CID_REPLY, num)


def log_num_follow():
    num = Follow.raw_sql('select count(1) from follow').fetchone()[0]
    log_history_new(Follow, LOG_HISTORY_CID_FOLLOW, num)


def log_num():
    log_num_user()
    log_num_reply()
    log_num_po()
    log_num_follow()
    log_num_po_zsite()
    log_part_time()


if __name__ == '__main__':
    #c = LogHistory.raw_sql(
    #    'select day , incr, num from log_history where cid=%s order by day desc limit %s', LOG_HISTORY_CID_REPLY, 100
    #).fetchall()
    #print c
    #log_num()
    data, user_id = log_incr_list(6, limit=100)
    print max(data)
