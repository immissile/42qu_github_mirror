#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McCacheA, McLimitA, McNum
from time import time
from cid import CID_INVITE_REGISTER, CID_NOTICE_REGISTER, CID_NOTICE_WALL, CID_NOTICE_WALL_REPLY, CID_INVITE_QUESTION, CID_NOTICE_QUESTION
from state import STATE_DEL, STATE_APPLY, STATE_ACTIVE
from po import Po
from zsite import Zsite
from wall import Wall, WallReply
from kv import Kv
from zkit.ordereddict import OrderedDict
from collections import defaultdict

STATE_GTE_APPLY = 'state>=%s' % STATE_APPLY

NOTICE_DIC = {
    CID_NOTICE_WALL: Wall,
    CID_NOTICE_WALL_REPLY: WallReply,
    CID_INVITE_QUESTION: Po,
    CID_NOTICE_QUESTION: Po,
}

notice_unread = Kv('notice_unread', 0)

def notice_unread_incr(user_id):
    unread = notice_unread.get(user_id)
    notice_unread.set(user_id, unread + 1)

def notice_unread_decr(user_id):
    unread = notice_unread.get(user_id)
    notice_unread.set(user_id, max(unread - 1, 0))

class Notice(McModel):
    @property
    def link(self):
        if not hasattr(self, '_link'):
            cls = NOTICE_DIC.get(self.cid)
            if cls:
                link = cls.mc_get(self.rid).link
            else:
                link = None
            self._link = link
        return self._link

    def rm(self, to_id):
        if self.to_id == to_id:
            state = self.state
            if state > STATE_DEL:
                self.state = STATE_DEL
                self.save()
                mc_flush(to_id)
                if state == STATE_APPLY:
                    notice_unread_decr(to_id)
                return True

    def read(self, to_id):
        if self.to_id == to_id:
            state = self.state
            if self.state == STATE_APPLY:
                self.state = STATE_ACTIVE
                self.save()
                notice_unread_decr(to_id)
                return True

def notice_new(from_id, to_id, cid, rid=0, state=STATE_APPLY):
    n = Notice(
        from_id=from_id,
        to_id=to_id,
        cid=cid,
        rid=rid,
        state=state,
        create_time=int(time()),
    )
    n.save()
    mc_flush(to_id)
    notice_unread_incr(to_id)
    return n

def invite_question(from_id, to_id, qid):
    n = notice_new(from_id, to_id, CID_INVITE_QUESTION, qid)
    return n

notice_count = McNum(lambda to_id: Notice.where(to_id=to_id).where(STATE_GTE_APPLY).count(), 'NoticeCount.%s')

mc_notice_id_list = McLimitA('NoticeIdList.%s', 256)

@mc_notice_id_list('{to_id}')
def notice_id_list(to_id, limit, offset):
    return Notice.where(to_id=to_id).where('state>=%s' % STATE_APPLY).order_by('id desc').field_list(limit, offset)

def notice_list(to_id, limit, offset):
    li = Notice.mc_get_list(notice_id_list(to_id, limit, offset))
    dic = OrderedDict()
    cls_dic = defaultdict(set)
    for i in li:
        cls_dic[Zsite].add(i.from_id)
        cls_dic[NOTICE_DIC.get(i.cid)].add(i.rid)
    for cls, id_list in cls_dic.items():
        if cls:
            cls_dic[cls] = cls.mc_get_dict(id_list)
        else:
            cls_dic[cls] = {}
    for i in li:
        i.from_user = cls_dic[Zsite][i.from_id]
        i.entry = cls_dic[NOTICE_DIC.get(i.cid)].get(i.rid)
    return li

def mc_flush(to_id):
    to_id = str(to_id)
    mc_notice_id_list.delete(to_id)
    notice_count.delete(to_id)
