#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McCacheA, McLimitA, McNum
from time import time
from cid import CID_INVITE_REGISTER, CID_NOTICE_REGISTER, CID_NOTICE_WALL, CID_NOTICE_WALL_REPLY, CID_INVITE_QUESTION, CID_NOTICE_QUESTION, CID_NOTICE_PAY
from state import STATE_DEL, STATE_APPLY, STATE_ACTIVE
from po import Po
from zsite import Zsite
from wall import Wall, WallReply
from kv import Kv
from zkit.ordereddict import OrderedDict
from collections import defaultdict
from mail import rendermail, render_template, sendmail
from mail_notice import mail_notice_state
from career import career_dict
from user_mail import mail_by_user_id
from money import Trade
from zkit.attrcache import attrcache

STATE_GTE_APPLY = 'state>=%s' % STATE_APPLY

NOTICE_TUPLE = (
    (CID_NOTICE_WALL, Wall, None),
    (CID_NOTICE_WALL_REPLY, Wall, None),
    (CID_INVITE_QUESTION, Po, '/mail/notice/invite_question.txt'),
    (CID_NOTICE_QUESTION, Po, '/mail/notice/notice_question.txt'),
#    (CID_NOTICE_PAY, Trade, None),
)

NOTICE_CLS = dict(i[:2] for i in NOTICE_TUPLE)

NOTICE_MAIL_DAY = dict(i[:2] for i in NOTICE_TUPLE[:2])
#NOTICE_MAIL_DIC = dict((i[0], (i[1], i[2])) for i in NOTICE_TUPLE[2:])

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

    @attrcache
    def link_to(self):
        cls = NOTICE_CLS.get(self.cid)
        if cls:
            link = cls.mc_get(self.rid).link
            return link

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

    @attrcache
    def seq(self):
        return notice_id_count(self.from_id, self.to_id, self.cid, self.rid)


def notice_new(from_id, to_id, cid, rid, state=STATE_APPLY):
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
    mc_notice_id_count.delete('%s_%s_%s_%s' % (from_id, to_id, cid, rid))
    return n

mc_notice_id_count = McCache('NoticeIdCount.%s')

@mc_notice_id_count('{from_id}_{to_id}_{cid}_{rid}')
def notice_id_count(from_id, to_id, cid, rid):
    return Notice.where(from_id=from_id, to_id=to_id, cid=cid, rid=rid).count()

def notice_new_hide_old(from_id, to_id, cid, rid):
    if notice_id_count(from_id, to_id, cid, rid):
        for i in Notice.where(from_id=from_id, to_id=to_id, cid=cid, rid=rid):
            i.rm(to_id)
    return notice_new(from_id, to_id, cid, rid)

def notice_wall_new(from_id, to_id, wall_id):
    return notice_new_hide_old(from_id, to_id, CID_NOTICE_WALL, wall_id)

def notice_wall_reply_new(from_id, to_id, wall_id):
    return notice_new_hide_old(from_id, to_id, CID_NOTICE_WALL_REPLY, wall_id)

def invite_question(from_id, to_id, qid):
    from po_question import answer_id_get
    if not answer_id_get(to_id, qid):
        if not notice_id_count(from_id, to_id, CID_INVITE_QUESTION, qid):
            n = notice_new(from_id, to_id, CID_INVITE_QUESTION, qid)
            if mail_notice_state(to_id, CID_INVITE_QUESTION):
                mq_invite_question_mail(n)
            return n

def notice_question(to_id, qid):
    for from_id in Notice.where(cid=CID_INVITE_QUESTION, rid=qid, to_id=to_id).where(STATE_GTE_APPLY):
        n = notice_new(to_id, from_id, CID_NOTICE_QUESTION, qid)
        notice_question_mail(n)

from mq import mq_client
mq_notice_question = mq_client(notice_question)

def invite_question_mail(notice):
    from_id = notice.from_id
    to_id = notice.to_id
    rid = notice.rid
    mail = mail_by_user_id(to_id)
    name = Zsite.mc_get(to_id).name
    from_name = Zsite.mc_get(from_id).name
    question = Po.mc_get(rid)
    rendermail('/mail/notice/invite_question.txt', mail, name,
               entry=question,
               from_name=from_name,
               notice=notice,
              )

mq_invite_question_mail = mq_client(invite_question_mail)


def notice_question_mail(notice):
    from_id = notice.from_id
    to_id = notice.to_id
    rid = notice.rid
    mail = mail_by_user_id(to_id)
    name = Zsite.mc_get(to_id).name
    from_name = Zsite.mc_get(from_id).name
    question = Po.mc_get(rid)
    rendermail('/mail/notice/notice_question.txt', mail, name,
               entry=question,
               from_name=from_name,
               notice=notice,
              )


def notice_mail_day(to_id, li):
    from user_mail import mail_by_user_id

    to_user = Zsite.mc_get(to_id)
    name = to_user.name
    mail = mail_by_user_id(to_id)
    count = len(li)
    li_wall = []
    _li_wall_reply = defaultdict(list)

    for from_id, cid, rid in li:
        from_user = Zsite.mc_get(from_id)
        if cid == CID_NOTICE_WALL:
            li_wall.append(from_user)
        elif cid == CID_NOTICE_WALL_REPLY:
            o = Wall.mc_get(rid)
            _li_wall_reply[rid].append(from_user)

    li_wall_reply = {}

    for rid, from_list in _li_wall_reply.iteritems():
        o = Wall.mc_get(rid)
        li_wall_reply[o] = from_list

    if li_wall or li_wall_reply:

        subject = render_template(
            '/mail/notice/day_total.txt',
            count=count,
            li_wall=li_wall,
            li_wall_reply=li_wall_reply,
        )

        rendermail(
            '/mail/notice/day_total.htm',
            mail,
            name,
            to_user=to_user,
            li_wall=li_wall,
            li_wall_reply=li_wall_reply,
            format='html',
            subject=subject,
        )


notice_count = McNum(lambda to_id: Notice.where(to_id=to_id).where(STATE_GTE_APPLY).count(), 'NoticeCount.%s')

mc_notice_id_list = McLimitA('NoticeIdList.%s', 256)

@mc_notice_id_list('{to_id}')
def notice_id_list(to_id, limit, offset):
    return Notice.where(to_id=to_id).where('state>=%s' % STATE_APPLY).order_by('id desc').col_list(limit, offset)

def notice_list(to_id, limit, offset):
    li = Notice.mc_get_list(notice_id_list(to_id, limit, offset))
    dic = OrderedDict()
    cls_dic = defaultdict(set)
    for i in li:
        cls_dic[Zsite].add(i.from_id)
        cls_dic[NOTICE_CLS.get(i.cid)].add(i.rid)
    from_list = cls_dic[Zsite]
    for cls, id_list in cls_dic.items():
        if cls:
            cls_dic[cls] = cls.mc_get_dict(id_list)
        else:
            cls_dic[cls] = {}
    career_dic = career_dict(from_list)
    for i in li:
        from_id = i.from_id
        i.from_user = cls_dic[Zsite][from_id]
        i.from_user.career = career_dic[from_id]
        i.entry = cls_dic[NOTICE_CLS.get(i.cid)].get(i.rid)
    return li

def mc_flush(to_id):
    to_id = str(to_id)
    mc_notice_id_list.delete(to_id)
    notice_count.delete(to_id)

if __name__ == '__main__':
    pass
    to_user = Zsite.mc_get(10000000)
    rendermail(
        '/mail/notice/day_total.txt',
        'zsp007@gmail.com',
        'x',
        to_user=to_user,
        count=3,
        li_wall_reply={},
    )
