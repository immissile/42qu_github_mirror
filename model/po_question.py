#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import McCache, McNum
from cid import CID_WORD, CID_NOTE, CID_QUESTION, CID_ANSWER
from spammer import is_same_post
from po import Po, po_new, po_word_new, po_note_new, po_cid_set
from rank import rank_po_id_list, rank_new
from state import STATE_RM, STATE_SECRET
from txt import txt_new
from zkit.time_format import time_title
from zsite import Zsite
from model.notice import mq_notice_question


def po_question_new(user_id, name, txt, state, zsite_id):
    if not name and not txt:
        return
    name = name or time_title()
    if not is_same_post(user_id, name, txt, zsite_id):
        m = po_new(CID_QUESTION, user_id, name, state, zsite_id=zsite_id)
        if m:
            txt_new(m.id, txt)
            if state > STATE_SECRET:
                m.feed_new()
            return m

mc_answer_id_get = McCache('AnswerIdGet.%s')
answer_count = McNum(lambda id:Po.where(rid=id).where('state>%s', STATE_RM).count(), 'AnswerCount:%s')


@mc_answer_id_get('{user_id}_{question_id}')
def answer_id_get(user_id, question_id):
    for i in Po.where(user_id=user_id, rid=question_id).where('cid in (%s,%s)'%(CID_WORD, CID_ANSWER)).where('state>%s', STATE_RM).col_list(1, 0):
        return i
    return 0

def answer_word2note(po):
    rid = po.rid
    if rid and po.cid == CID_WORD:
        po_cid_set(po, CID_ANSWER)
        answer_count.delete(rid)

def po_answer_new(user_id, question_id, name, txt, state):
#    from buzz import buzz_answer_new
    id = answer_id_get(user_id, question_id)

    if id:
        return Po.mc_get(id)
    else:
        if txt:
            m = _po_answer_new(user_id, name, txt, state, question_id)
        else:
            m = po_word_new(user_id, name, state, question_id)

        if m:
            id = m.id
            #buzz_answer_new(user_id, question_id)
            rank_new(m, question_id, CID_QUESTION)
            mq_notice_question(user_id, id)
            mc_answer_id_get.set('%s_%s' % (user_id, question_id), id)
            answer_count.delete(question_id)
            return m


def _po_answer_new(user_id, name, txt, state, rid):
    if not name and not txt:
        return
    if not is_same_post(user_id, name, txt):
        m = po_new(CID_ANSWER, user_id, name, state, rid)
        if m:
            txt_new(m.id, txt)
            if state > STATE_SECRET:
                m.feed_new()
            return m

def po_user_id_list(question_id):
    question = Po.mc_get(question_id)
    user_id = question.user_id
    po_id_list = rank_po_id_list(question_id, CID_QUESTION, 'confidence')
    po_list = Po.mc_get_list(po_id_list)
    user_id_list = [i.user_id for i in po_list]
    user_id_list.append(user_id)
    return set(user_id_list)

def po_answer_list(question_id, zsite_id=0, user_id=0):
    ids = rank_po_id_list(question_id, CID_QUESTION, 'confidence')

    if zsite_id == user_id:
        zsite_id = 0

    user_ids = filter(bool, (zsite_id, user_id))
    if user_ids:
        _ids = []
        for i in user_ids:
            user_answer_id = answer_id_get(i, question_id)
            if user_answer_id:
                _ids.append(user_answer_id)
                if user_answer_id in ids:
                    ids.remove(user_answer_id)
        if _ids:
            _ids.extend(ids)
            ids = _ids

    li = Po.mc_get_list(ids)
    Zsite.mc_bind(li, 'user', 'user_id')
    return li


