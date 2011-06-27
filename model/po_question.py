#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import McCache
from cid import CID_QUESTION
from spammer import is_same_post
from po import Po, po_new, po_word_new, po_note_new, po_rm, CID_QUESTION
from rank import rank_po_id_list, rank_new
from state import STATE_DEL, STATE_SECRET, STATE_ACTIVE
from txt import txt_new, txt_get
from zsite import Zsite
from model.notice import mq_notice_question

def po_question_new(user_id, name, txt, state):
    if not name and not txt:
        return
    if not is_same_post(user_id, name, txt):
        m = po_new(CID_QUESTION, user_id, name, 0, state)
        txt_new(m.id, txt)
        m.feed_new()
        return m

mc_answer_id_get = McCache('AnswerIdGet.%s')

@mc_answer_id_get('{user_id}_{question_id}')
def answer_id_get(user_id, question_id):
    for i in Po.where(user_id=user_id, rid=question_id).col_list(1, 0):
        return i
    return 0

def po_answer_new(user_id, question_id, name, txt, state):
    if not answer_id_get(user_id, question_id):
        if txt:
            m = po_note_new(user_id, name, txt, state, question_id)
        else:
            m = po_word_new(user_id, name, state, question_id)
        if m:
            id = m.id
            rank_new(m, question_id, CID_QUESTION)
            mq_notice_question(user_id, id)
            mc_answer_id_get.set('%s_%s' % (user_id, question_id), id)
            return m



def po_answer_list(question_id, zsite_id=0, user_id=0):
    ids = rank_po_id_list(question_id, CID_QUESTION, 'confidence')


    if zsite_id == user_id:
        zsite_id = 0

    user_ids = filter(bool, (zsite_id, user_id))
    if user_ids:
        _ids = []
        for i in user_ids:
            user_answer_id = answer_id_get(user_id, question_id)
            if user_answer_id:
                _ids.append(user_answer_id)
                ids.remove(user_answer_id) 
        if _ids:
            _ids.extend(ids)
            ids = _ids

    li = Po.mc_get_list(ids)
    Zsite.mc_bind(li, 'user', 'user_id')
    return li







