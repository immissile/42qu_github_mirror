#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cid import CID_QUESTION, CID_ANSWER
from spammer import is_same_post
from po import po_new, po_rm, CID_QUESTION, CID_ANSWER
from rank import rank_po_id_list, rank_new
from state import STATE_DEL, STATE_SECRET, STATE_ACTIVE
from txt import txt_new, txt_get

def po_question_new(user_id, name, txt):
    if not is_same_post(user_id, name, txt):
        m = po_new(CID_QUESTION, user_id, name, STATE_ACTIVE)
        txt_new(m.id, txt)
        m.feed_new()
        return m

def po_answer_new(user_id, question_id, name, txt):
    if not is_same_post(user_id, name, txt):
        m = po_new(CID_ANSWER, user_id, name, STATE_ACTIVE)
        txt_new(m.id, txt)
        rank_new(m, question_id, CID_ANSWER)
        m.feed_new()
        return m

def po_answer_list(question_id):
    return rank_po_id_list(question_id, CID_ANSWER, 'confidence')
