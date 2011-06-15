#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McCacheA, McLimitA, McNum
from time import time
from cid import CID_INVITE_REGISTER, CID_NOTICE_REGISTER, CID_INVITE_QUESTION, CID_NOTICE_QUESTION
from state import STATE_DEL, STATE_APPLY, STATE_ACTIVE
from po import Po

STATE_GTE_APPLY = 'state>=%s' % STATE_APPLY

NOTICE_DIC = {
    CID_INVITE_QUESTION: Po,
    CID_notice_QUESTION: Po,
}

class Notice(McModel):
    pass

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
    return n

def invite_question(from_id, to_id, qid):
    n = notice_new(from_id, to_id, CID_INVITE_QUESTION, qid)
    return n

notice_unread_count = McNum(lambda to_id: Notice.where(to_id=to_id, state=STATE_APPLY).count(), 'NoticeUnreadCount.%s')
notice_count = McNum(lambda to_id: Notice.where(to_id=to_id).where(STATE_GTE_APPLY).count(), 'NoticeCount.%s')

mc_notice_id_list = McLimitA('NoticeIdList.%s')

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

def notice_rm(to_id, notice_id):
    n = Notice.mc_get(notice_id)
    if n and n.to_id = to_id and n.state > STATE_DEL:
        n.state = STATE_DEL
        n.save()
        mc_flush(to_id)
        return True

def mc_flush(to_id):
    to_id = str(to_id)
    mc_notice_id_list.delete(to_id)
    notice_unread_count.delete(to_id)
    notice_count.delete(to_id)
