#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import McCache
from cid import CID_QUESTION, CID_ANSWER
from spammer import is_same_post
from po import Po, po_new, po_word_new, po_note_new, po_rm, CID_QUESTION
from rank import rank_po_id_list, rank_new
from state import STATE_DEL, STATE_SECRET, STATE_ACTIVE
from txt import txt_new, txt_get

def po_question_new(user_id, name, txt, state):
    if not is_same_post(user_id, name, txt):
        m = po_new(CID_QUESTION, user_id, name, 0, state)
        txt_new(m.id, txt)
        m.feed_new()
        return m

mc_answer_id_get = McCache('AnswerIdGet.%s')

@mc_answer_id_get('{user_id}_{question_id}')
def answer_id_get(user_id, question_id):
    for i in Po.where(user_id=user_id, rid=question_id).field_list(1, 0):
        return i
    return 0

def po_answer_new(user_id, question_id, name, txt, state):
    if not answer_id_get(user_id, question_id):
        if txt:
            m = po_note_new(user_id, name, txt, state, question_id)
        else:
            m = po_word_new(user_id, name, state, question_id)
        if m:
            rank_new(m, question_id, CID_QUESTION)
            return m

def po_answer_list(question_id):
    ids = rank_po_id_list(question_id, CID_QUESTION, 'confidence')
    return Po.mc_get_list(ids)
