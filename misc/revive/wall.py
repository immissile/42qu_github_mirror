#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from qu.mysite.model.man_wall import ManWall, ManWallReply
from qu.mysite.util.orm import ormiter
from model.zsite import Zsite
from model.wall import Wall, wall_id_by_from_id_to_id, mc_wall_id_by_from_id_to_id
from model.state import STATE_DEL, STATE_SECRET, STATE_ACTIVE
from model.zsite_tag import zsite_tag_new_by_tag_name
from model.po_question import po_answer_new
from mysite.model.vote_review import VoteReview
from model.vote import vote_up

USER_ID = 10000000

def init_wall():
    for o in ormiter(ManWall, 'state>3'):
        from_id = o.from_id
        to_id = o.to_id
        from_ = Zsite.mc_get(from_id)
        to = Zsite.mc_get(to_id)
        if from_ and to:
            w = Wall.get(from_id=from_id, to_id=to_id)
            to.reply_new(from_, 
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
    init_wall()
