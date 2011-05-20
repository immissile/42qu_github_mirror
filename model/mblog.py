#!/usr/bin/env python
#coding:utf-8
from _db import cursor_by_table, McModel, McLimitA, McCache
from time import time

class Mblog(McModel):
    pass

MBLOG_CID_WORD = 1
MBLOG_CID_NOTE = 2

MBLOG_STATE_DEL = 3
MBLOG_STATE_SECRET = 7
MBLOG_STATE_ACTIVE = 10

mc_mblog_word_lastest = McCache("MblogWordLastest:%s")

@mc_mblog_word_lastest("{user_id}")
def mblog_word_lastest(user_id):
    c = Mblog.raw_sql(
            "select name from mblog where cid=%s and user_id=%s and state>=%s order by id desc limit 1",
            MBLOG_CID_WORD,
            user_id,
            MBLOG_STATE_ACTIVE
        )
    r = c.fetchone()
    if r:
        r = r[0]
    else:
        r = ''
    return r

def mblog_word_new( user_id, name, create_time=None):
    if create_time is None:
        create_time = int(time())
    if name.rstrip() and name != mblog_word_lastest(user_id):
        m = Mblog(
            name=name,
            user_id=user_id,
            create_time=create_time,
            cid=MBLOG_CID_WORD,
            state=MBLOG_STATE_ACTIVE
        )
        m.save()
        mc_mblog_word_lastest.set(user_id, name)
        return m

if __name__ == "__main__":
    print mblog_word_new( 1,"test",)

