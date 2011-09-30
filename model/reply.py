#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gid import gid
from _db import cursor_by_table, McModel, McLimitA, McCache
from txt import txt_new
from spammer import is_same_post, is_spammer, mc_lastest_hash
from time import time
from txt import txt_bind, txt_get
from model.txt2htm import txt_withlink
from state import STATE_DEL, STATE_APPLY, STATE_SECRET, STATE_ACTIVE
from cid import CID_PO
from zkit.attrcache import attrcache

REPLY_STATE = (
    STATE_DEL,
    STATE_APPLY,
    STATE_ACTIVE,
)

mc_reply_id_list = McLimitA('ReplyIdList:%s', 512)
mc_reply_id_list_reversed = McLimitA('ReplyIdListReversed:%s', 512)
mc_reply_count = McCache('ReplyCount:%s')
#mc_reply_in_1h = McCache('ReplyInOneHour.%s')

class ReplyMixin(object):
    reply_cursor = cursor_by_table('reply')

    def reply_new(self, user, txt, state=STATE_ACTIVE, create_time=None):
        from zsite import user_can_reply
        user_id = user.id

    #    if not user_can_reply(user):
    #        return
        if is_spammer(user_id):
            return

        txt = txt.rstrip()
        cid = self.cid
        rid = self.id
        if not txt or is_same_post(user_id, cid, rid, txt, state):
            return

        id = gid()
        if not create_time:
            create_time = int(time())
        txt_new(id, txt)
        cursor = self.reply_cursor
        cursor.execute(
            'insert into reply (id,cid,create_time,state,rid,user_id) values (%s,%s,%s,%%s,%%s,%%s)' % (
                id,
                cid,
                create_time,
            ),
            (state, rid, user_id)
        )
        cursor.connection.commit()
        mc_flush_reply_id_list(cid, rid)
        if cid in CID_PO:
            from buzz import mq_buzz_po_reply_new
            from po_pos import po_pos_state, STATE_BUZZ
            po_pos_state(user_id, rid, STATE_BUZZ)
            mq_buzz_po_reply_new(user_id, id, rid, self.user_id)
#            key = '%s_%s' % (rid, user_id)
#            if mc_reply_in_1h.get(key) is None:
#                mq_buzz_po_reply_new(user_id, rid)
#                mc_reply_in_1h.set(key, True, 3600)
        return id

    @property
    @mc_reply_count('{self.cid}_{self.id}')
    def reply_count(self):
        cid = self.cid
        rid = self.id
        cursor = self.reply_cursor
        cursor.execute('select count(1) from reply where rid=%s and cid=%s and state>=%s', (rid, cid, STATE_SECRET))
        r = cursor.fetchone()
        return r[0]


    def _reply_id_list(self, limit, offset, order):
        cursor = self.reply_cursor
        cid = self.cid
        rid = self.id

        sql = [
            'select id from reply where rid=%s and cid=%s',
            'and state>=%s'%STATE_SECRET
        ]

        para = [
            rid,
            cid
        ]
        sql.append(order)

        if limit:
            sql.append('limit %s')
            para.append(limit)

        if offset:
            sql.append('offset %s')
            para.append(offset)

        cursor.execute(
            ' '.join(sql), para
        )
        return [i for i, in cursor]

    @property
    def reply_id_last(self):
        li = self.reply_id_list_reversed(1, 0)
        if li:
            return li[0]
        return 0

    @mc_reply_id_list_reversed('{self.cid}_{self.id}')
    def reply_id_list_reversed(self, limit=None, offset=None):
        return self._reply_id_list(limit, offset, 'order by id desc')

    @mc_reply_id_list('{self.cid}_{self.id}')
    def reply_id_list(self, limit=None, offset=None):
        return self._reply_id_list(limit, offset, 'order by id')

    def _reply_list(self, limit, offset, reply_id_list):
        from model.zsite import Zsite
        r = Reply.mc_get_list(
            reply_id_list(limit, offset)
        )
        txt_bind(r)
        Zsite.mc_bind(r, 'user', 'user_id')
        return r

    def reply_list_reversed(self, limit=None, offset=None):
        return self._reply_list(limit, offset, self.reply_id_list_reversed)

    def reply_list(self, limit=None, offset=None):
        return self._reply_list(limit, offset, self.reply_id_list)

class Reply(McModel):
    @attrcache
    def txt(self):
        return txt_get(self.id)

    @property
    def htm(self):
        return txt_withlink(self.txt)

    def rm(self):
        from buzz import mq_buzz_po_reply_rm
        if self.state != STATE_DEL:
            self.state = STATE_DEL
            self.save()
            mc_flush_reply_id_list(self.cid, self.rid)
            mq_buzz_po_reply_rm(self.id)

        user_id = self.user_id
        mc_lastest_hash.delete(user_id)

    def can_rm(self, user_id):
        return self.user_id == user_id


def mc_flush_reply_id_list(cid, rid):
    key = '%s_%s' % (cid, rid)
    mc_reply_id_list.delete(key)
    mc_reply_id_list_reversed.delete(key)
    mc_reply_count.delete(key)

if __name__ == '__main__':
    pass
