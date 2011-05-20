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

def mblog_word_new(name, user_id, create_time=None):
    if create_time is None:
        create_time = int(time())

    Mblog(
        name=name,
        user_id=user_id,
        create_time=create_time,
        cid=MBLOG_CID_WORD,
        state=MBLOG_STATE_ACTIVE
    )


