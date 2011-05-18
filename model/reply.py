#!/usr/bin/env python
#coding:utf-8
from gid import gid
from _db import cursor_by_table, McModel, McLimitA
from txt import txt_new
from spammer import is_spammer
from time import time


REPLY_STATE_DEL = 3
REPLY_STATE_APPLY = 5
REPLY_STATE_ACTIVE = 10

REPLY_STATE = (
    REPLY_STATE_DEL,
    REPLY_STATE_APPLY,
    REPLY_STATE_ACTIVE,
)

mc_reply_id_list = McLimitA("ReplyIdList:%s", 512)

class ReplyMixin(object):
    reply_cursor = cursor_by_table('reply')

    def reply_new(self, user_id, txt, state=REPLY_STATE_ACTIVE):
        txt = txt.rstrip()
        if not txt or is_spammer(user_id):
            return
        cid = self.TID
        rid = self.id

        id = gid()
        txt_new(id, txt)
        cursor = self.reply_cursor
        cursor.execute(
            "insert into reply (id,cid,create_time,state,rid,user_id) values (%s,%s,%s,%%s,%%s,%%s)"%(
                id,
                cid,
                int(time())
            ),
            (state, rid, user_id)
        )
        cursor.connection.commit()
        mc_flush_reply_id_list(cid,rid)
        return id

    def reply_id_list(self, user_id=None):
        id = self.id
        if id == user_id:
            state = REPLY_STATE_APPLY
        else:
            state = REPLY_STATE_ACTIVE
        cursor = self.reply_cursor
        return _reply_id_list(self.TID, id, state)

class Reply(McModel):
    pass

def mc_flush_reply_id_list(cid, rid):
    key = "%s_%s_%%s"%(cid,rid)
    for i in REPLY_STATE:
        mc_reply_id_list.delete(key%i)

@mc_reply_id_list("{cid}_{rid}_{state}")
def _reply_id_list(cid, rid, state, cursor=None):
    if cursor is None:
        cursor = cursor_by_table('reply')
    cursor.execute(
        "select id from reply where state>=%s and rid=%s and cid=%s",
        state,
        rid,
        cid
    )


if __name__ == "__main__":
    from _db import exe_sql
    def create_reply_table_sql(table):
        pass







