#!/usr/bin/env python
#coding:utf-8
from gid import gid
from _db import cursor_by_table, McModel, McLimitA, McCache
from txt import txt_new
from spammer import is_spammer
from time import time
from txt import txt_bind
from zkit.txt2htm import txt_withlink

REPLY_STATE_DEL = 3
REPLY_STATE_APPLY = 5
REPLY_STATE_SECRET = 7
REPLY_STATE_ACTIVE = 10

REPLY_STATE = (
    REPLY_STATE_DEL,
    REPLY_STATE_APPLY,
    REPLY_STATE_ACTIVE,
)

mc_reply_id_list = McLimitA("ReplyIdList:%s", 512)
mc_reply_total = McCache("ReplyTotal:%s")

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

    @property
    @mc_reply_total("{self.TID}_{self.id}")
    def reply_total(self):
        cid = self.TID
        rid = self.id
        cursor = self.reply_cursor
        cursor.execute("select count(1) from reply where rid=%s and cid=%s and state>=%s", (rid, cid, REPLY_STATE_SECRET))
        r = cursor.fetchone()
        return r[0]

    @mc_reply_id_list("{self.TID}_{self.id}")
    def reply_id_list(self, limit=None, offset=None):
        cursor = self.reply_cursor
        cid = self.TID
        rid = self.id

        sql = [
            "select id from reply where rid=%s and cid=%s",
            "and state>=%s"%REPLY_STATE_SECRET
        ]

        para = [
            rid,
            cid
        ]
        sql.append("order by id desc")

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

    def reply_list(self, limit=None, offset=None):
        from model.zsite import Zsite
        r = Reply.mc_get_list(
            self.reply_id_list(limit, offset)
        )
        txt_bind(r)
        Zsite.mc_bind(r, "user", "user_id")
        return r

class Reply(McModel):
    @property
    def htm(self):
        return txt_withlink(self.txt)

def mc_flush_reply_id_list(cid, rid):
    key = "%s_%s"%(cid, rid)
    mc_reply_id_list.delete(key)
    mc_reply_total.delete(key)

if __name__ == "__main__":
    pass
