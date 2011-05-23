#!/usr/bin/env python
#coding:utf-8
from _db import cursor_by_table, McModel, McLimitA, McCache
from time import time
from cid import CID_WORD, CID_NOTE, CID_QUESTION, CID_ANSWER
from feed import feed_entry_new, mc_feed_entry_tuple
from gid import gid
from txt import txt_new
from spammer import is_same_post
from datetime import datetime
from zkit.time_format import time_title

class Mblog(McModel):
    pass

MBLOG_STATE_DEL = 3
MBLOG_STATE_SECRET = 7
MBLOG_STATE_ACTIVE = 10


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

def mblog_edit_name(id, name):
    m = Mblog.mc_get(id)
    if m is None:return
    name = name.strip()
    if m.name != name and name:
        m.name = name
        m.save()

def mblog_rm(user_id, id):
    m = Mblog.mc_get(id)
    if m.user_id == user_id:
        m.state == MBLOG_STATE_DEL
        m.save()
        feed_entry_rm(id)

@mc_feed_entry_tuple('{id}')
def feed_tuple_word(id):
    m = Mblog.mc_get(id)
    if m:
        return (m.name, )
    return False

def mblog_word_new(user_id, name):
    name = name.strip()
    if name and not is_same_post(user_id, name):
        m = mblog_new(CID_WORD, user_id, name, MBLOG_STATE_ACTIVE)
        id = m.id
        feed_entry_new(id, user_id, CID_WORD)
        return m

#def mblog_question_new(user_id, name , txt):
#    m = mblog_new(CID_QUESTION, user_id, name, MBLOG_STATE_SECRET)
#    txt_new(m.id, txt)
#    return m

def mblog_note_new(user_id, name, txt, state):
    name = name.strip() or time_title()
    if is_same_post(user_id, name, txt):
        return
    m = mblog_new(CID_NOTE, user_id, name, state)
    txt_new(m.id, txt)
    return m



if __name__ == "__main__":
    #print mblog_word_new( 1, "test", )
    name = str(datetime.now())[:16]
    print name
