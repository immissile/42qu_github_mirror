#!/usr/bin/env python
#coding:utf-8
from _db import cursor_by_table, McModel, McLimitA, McCache
from time import time
from cid import CID_WORD, CID_NOTE
from feed import feed_entry_new
from gid import gid
from txt import txt_new

class Mblog(McModel):
    pass


MBLOG_STATE_DEL = 3
MBLOG_STATE_SECRET = 7
MBLOG_STATE_ACTIVE = 10

mc_mblog_word_lastest = McCache("MblogWordLastest:%s")

@mc_mblog_word_lastest("{user_id}")
def mblog_word_lastest(user_id):
    c = Mblog.raw_sql(
            "select name from mblog where cid=%s and user_id=%s and state>=%s order by id desc limit 1",
            CID_WORD,
            user_id,
            MBLOG_STATE_ACTIVE
        )
    r = c.fetchone()
    if r:
        r = r[0]
    else:
        r = ''
    return r


def mblog_new(cid, user_id, name, state):
    m = Mblog(
        id=gid(),
        name=name.strip(),
        user_id=user_id,
        create_time=int(time()),
        cid=CID_WORD,
        state=state
    )
    m.save()
    return m

def edit_name(id, name):
    m = Mblog.mc_get(id)
    if m is None:return
    name = name.strip()
    if m.name != name and name:
        m.name = name
        m.save()

def mblog_word_new(user_id, name):
    if name.rstrip() and name != mblog_word_lastest(user_id):
        m = mblog_new(CID_WORD, user_id, name, MBLOG_STATE_ACTIVE)
        mc_mblog_word_lastest.set(user_id, name)
        feed_entry_new(id, user_id, CID_WORD)
        return m

def mblog_question_new(user_id, name , txt):
    m = mblog_new(CID_WORD, user_id, name, MBLOG_STATE_SECRET)
    txt_new(m.id, txt)
    return m



if __name__ == "__main__":
    print mblog_word_new( 1, "test", )

