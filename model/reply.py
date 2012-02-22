#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gid import gid
from _db import cursor_by_table, McModel, McLimitA, McCache, McCacheA
from spammer import is_same_post, is_spammer, mc_lastest_hash
from time import time
from txt import txt_bind, txt_get, txt_new
from model.txt2htm import txt_withlink
from state import STATE_RM, STATE_APPLY, STATE_SECRET, STATE_ACTIVE
from cid import CID_PO, CID_SITE, CID_COM
from zkit.attrcache import attrcache
from user_mail import mail_by_user_id
from mail import rendermail
from buzz_reply import mq_buzz_po_reply_rm , mq_buzz_po_reply_new

REPLY_STATE = (
    STATE_RM,
    STATE_APPLY,
    STATE_ACTIVE,
)

mc_reply_id_list = McLimitA('ReplyIdList:%s', 512)
mc_reply_id_list_reversed = McLimitA('ReplyIdListReversed:%s', 512)
mc_reply_count = McCache('ReplyCount:%s')
#mc_reply_in_1h = McCache('ReplyInOneHour.%s')
mc_reply_zsite_id_list = McCacheA('ReplyZsiteIdList:%s')

class ReplyMixin(object):
    reply_cursor = cursor_by_table('reply')

    @mc_reply_zsite_id_list('{self.cid}_{self.id}')
    def reply_zsite_id_list(self):
        id_set = set()
        id_set.update(
            i.user_id for i in self.reply_list()
        )
        return list(id_set)

    def reply_new(self, user, txt, state=STATE_ACTIVE, create_time=None):
        from zsite import user_can_reply
        from po_tag import section_rank_refresh
        user_id = user.id
        cid = self.cid
        if cid not in (CID_SITE, CID_COM):
            if not user_can_reply(user):
                return
        if is_spammer(user_id):
            return

        txt = txt.rstrip()
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

#            key = '%s_%s' % (rid, user_id)
#            if mc_reply_in_1h.get(key) is None:
#                mq_buzz_po_reply_new(user_id, rid)
#                mc_reply_in_1h.set(key, True, 3600)
        if cid in CID_PO:
            section_rank_refresh(self)

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

    def reply_last(self):
        id = self.reply_id_last
        if id:
            return Reply.mc_get(id)

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

    def txt_set(self, txt):
        return txt_new(self.id, txt)


    @property
    def htm(self):
        return txt_withlink(self.txt)

    def rm(self):
        if self.state != STATE_RM:
            self.state = STATE_RM
            self.save()
            mc_flush_reply_id_list(self.cid, self.rid)
            mq_buzz_po_reply_rm(self.rid, self.id)

        user_id = self.user_id
        mc_lastest_hash.delete(user_id)

    def can_admin(self, user_id):
        if user_id:
            return self.user_id == user_id


def mc_flush_reply_id_list(cid, rid):
    key = '%s_%s' % (cid, rid)
    mc_reply_id_list.delete(key)
    mc_reply_id_list_reversed.delete(key)
    mc_reply_count.delete(key)
    mc_reply_zsite_id_list.delete(key)



if __name__ == '__main__':
    r = Reply.raw_sql('select *,count(rid) from reply where cid = 62 group by rid order by count(rid) desc limit 50').fetchall()
    from po import Po
    p_l,c_l = [],[]
    for i in r:
        p_l.append(i[1])
        c_l.append(i[-1])
    p = Po.mc_get_list(p_l)
    p = filter(lambda x:x,p)
    p = map(lambda x:(x.name,x.txt,'http:%s'%x.link),p)
    res = zip(p,c_l[1:])
    for n,((i,l,j),k) in enumerate(res):
        print '#'*20
        print '第%s名：'%(n+1),i,j,'\n','回复数:',k,
        print l,'\n\n'
    pass
