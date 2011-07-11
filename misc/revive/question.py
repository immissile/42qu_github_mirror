#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from qu.mysite.model.question import question_id_list, Question
from model.po import po_new, CID_QUESTION,txt_new
from model.state import STATE_DEL, STATE_SECRET, STATE_ACTIVE
from model.zsite_tag import zsite_tag_new_by_tag_name
from model.po_question import po_answer_new
from qu.mysite.model import review 
from mysite.model.vote_review import VoteReview
from model.vote import vote_up

USER_ID = 10000000

def init_question():
    question_id_dict = {}
    for question in reversed(Question.mc_get_list(question_id_list())):
        m = po_new(CID_QUESTION, USER_ID, question.title, STATE_ACTIVE)
        txt_new(m.id, question.txt)
        zsite_tag_new_by_tag_name(m, "沉思录")
 
        question_id_dict[question.id] = m.id

    for i in review.Review.where("state>%s"%review.STATE_DEL):
        if i.to_id in question_id_dict:
            question_id = question_id_dict[i.to_id]

            q = po_answer_new(i.from_id, question_id, i.title, i.txt, STATE_ACTIVE)
            
            for i in VoteReview.where(review_id=i.id):
                print i.man_id, q.id
                vote_up(i.man_id, q.id)


if __name__ == '__main__':
    init_question()

    pass

