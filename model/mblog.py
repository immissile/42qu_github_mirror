#!/usr/bin/env python
#coding:utf-8
from _db import cursor_by_table, McModel, McLimitA, McCache
from time import time
from cid import CID_WORD, CID_NOTE, CID_QUESTION, CID_ANSWER
from feed import feed_entry_new, mc_feed_entry_tuple
from gid import gid
from txt import txt_new, txt_get
from spammer import is_same_post
from datetime import datetime
from zkit.time_format import time_title


MBLOG_STATE_DEL = 3
MBLOG_STATE_SECRET = 7
MBLOG_STATE_ACTIVE = 10

MBLOG_LINK = {
    CID_NOTE : "/note/%s",
    CID_WORD : "/word/%s",
}

class Mblog(McModel):
    @property
    def txt(self):
        return txt_get(self.id)

    @property
    def link(self):
        id = self.id
        cid = self.cid
        if not hasattr(self, "_link"):
            self._link = MBLOG_LINK[cid]%id
        return self._link

    def can_admin(self, user_id):
        return self.user_id == user_id

def mblog_new(cid, user_id, name, state):
    m = Mblog(
        id=gid(),
        name=name,
        user_id=user_id,
        create_time=int(time()),
        cid=cid,
        state=state
    )
    m.save()
    return m

def mblog_edit_name(id, name):
    m = Mblog.mc_get(id)
    if m is None:return
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
def feed_tuple_note(id):
    m = Mblog.mc_get(id)
    if m:
        return (m.name, m.txt)
    return ()

@mc_feed_entry_tuple('{id}')
def feed_tuple_word(id):
    m = Mblog.mc_get(id)
    if m:
        return (m.name, )
    return False

def mblog_word_new(user_id, name):
    if name and not is_same_post(user_id, name):
        m = mblog_new(CID_WORD, user_id, name, MBLOG_STATE_ACTIVE)
        id = m.id
        feed_entry_new(id, user_id, CID_WORD)
        return m

#def mblog_question_new(user_id, name , txt):
#    m = mblog_new(CID_QUESTION, user_id, name, MBLOG_STATE_SECRET)
#    txt_new(m.id, txt)
#    return m

def mblog_note_can_view(mblog, user_id):
    if not mblog:
        return False
    if mblog.state <= MBLOG_STATE_DEL:
        return False
    if mblog.cid != CID_NOTE:
        return False
    if mblog.state == MBLOG_STATE_SECRET:
        if mblog.user_id != user_id:
            return False
    return True

def mblog_note_new(user_id, name, txt, state):
    name = name or time_title()
    if is_same_post(user_id, name, txt):
        return
    m = mblog_new(CID_NOTE, user_id, name, state)
    id = m.id
    txt_new(id, txt)
    if state > MBLOG_STATE_SECRET:
        feed_entry_new(id, user_id, CID_NOTE)
    return m



if __name__ == "__main__":
    #print mblog_word_new( 1, "test", )
    name = str(datetime.now())[:16]
    print name
