#!/usr/bin/env python
#coding:utf-8
from gid import gid
from _db import cursor_by_table, McModel, McLimitA
from txt import txt_new
from spammer import is_spammer
from time import time
from txt import txt_bind

REPLY_STATE_DEL = 3
REPLY_STATE_APPLY = 5
REPLY_STATE_APPLYED = 7
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
        mc_flush_reply_id_list(cid, rid)
        return id

    @mc_reply_id_list("{self.TID}_{self.id}_{state}")
    def reply_id_list(self, state=None, limit=None, offset=None):
        cursor = self.reply_cursor
        cid = self.TID
        rid = self.id

        sql = [
            "select id from reply where state>=%s and rid=%s and cid=%s"
        ]

        para = [
                state,
                rid,
                cid
        ]

        if limit:
            sql.append("limit %s")
            para.append(limit)

        if offset:
            sql.append("offset %s")
            para.append(offset)

        cursor.execute(
            " ".join(sql), para
        )
        return [i for i, in cursor]


    def reply_list(self, user_id=None):
        r = Reply.mc_get_list(
            self.reply_id_list(user_id)
        )
        txt_bind(r)
        return r

class Reply(McModel):
    pass

def mc_flush_reply_id_list(cid, rid):
    key = "%s_%s_%%s"%(cid, rid)
    for i in REPLY_STATE:
        mc_reply_id_list.delete(key%i)

if __name__ == "__main__":
    pass






