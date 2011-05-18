#!/usr/bin/env python
#coding:utf-8
from gid import gid
from _db import cursor_by_table
from txt import txt_new
from spammer import is_spammer
from time import time

REPLY_STATE_DEL = 3
REPLY_STATE_ACTIVE = 10



class ReplyMixin(object):
    def reply_new(self, user_id, txt, state=REPLY_STATE_ACTIVE):
        txt = txt.rstrip()
        if not txt or is_spammer(user_id):
            return
        table = "%s_reply"%self.Meta.table
        cursor = cursor_by_table(table)
        rid = self.id
        id = gid()
        txt_new(id, txt)
        cursor.execute(
            "insert into reply (id,cid,create_time,state,rid,user_id) values (%s,%s,%s,%%s,%%s,%%s)"%(
                id,
                self.TID,
                int(time())
            ),
            (state, rid, user_id)
        )
        cursor.connection.commit()
        return id

if __name__ == "__main__":
    from _db import exe_sql
    def create_reply_table_sql(table):
        pass







