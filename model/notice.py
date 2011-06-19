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
    CID_NOTICE_WALL_REPLY: Wall,
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
        return '/notice/%s' % self.id

    @property
    def link_to(self):
        if not hasattr(self, '_link_to'):
            cls = NOTICE_DIC.get(self.cid)
            if cls:
                link = cls.mc_get(self.rid).link
            else:
                link = None
            self._link_to = link
        return self._link_to

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

mc_notice_id_get = McCache('NoticeIdGet.%s')

@mc_notice_id_get('{from_id}_{to_id}_{cid}_{rid}')
def notice_id_get(from_id, to_id, cid, rid):
    n = Notice.get(from_id=from_id, to_id=to_id, cid=CID_INVITE_QUESTION, rid=qid)
    if n:
        return n.id
    return 0

def invite_question(from_id, to_id, qid):
    nid = notice_id_get(from_id, to_id, CID_INVITE_QUESTION, qid)
    if not nid:
        n = notice_new(from_id, to_id, CID_INVITE_QUESTION, qid)
        return n

def invite_question_mail(notice):
    from model.user_mail import mail_by_user_id
    from model.mail import rendermail
    to_id = notice.to_id
    to_user = Zsite.mc_get(to_id)
    if to_user and notice_with_mail(to_id, CID_INVITE_QUESTION):
        mail = mail_by_user_id(to_id)
        name = to_user.name
        question = Po.mc_get(notice.rid)
        from_name = Zsite.mc_get(notice.from_id).name
        rendermail('/mail/notice/invite_question.txt', mail, name,
                   question=question,
                   from_name=from_name,
                   notice=notice,
                  )

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


class NoticeMail(Model):
    pass

mc_notice_with_mail = McCache('NoticeWithMail.%s')

@mc_notice_with_mail('{user_id}_{cid}')
def notice_with_mail(user_id, cid):
    m = NoticeMail.get(user_id=user_id, cid=cid)
    if not m:
        m = NoticeMail(user_id=user_id, cid=cid, state=1)
        m.save()
    return m.state

def notice_mail_set(user_id, cid, state):
    state = int(bool(state))
    NoticeMail.where(user_id=user_id, cid=cid).update(state=state)
    mc_notice_with_mail.set('%s_%s' % (user_id, cid), state)
