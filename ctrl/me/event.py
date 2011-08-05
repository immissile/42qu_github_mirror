#!/usr/bin/dev python
# -*- coding: utf-8 -*-
from _handler import LoginBase
from ctrl._urlmap.me import urlmap
from model import reply
from model.cid import CID_WORD, CID_NOTE, CID_QUESTION, CID_ANSWER
from model.po import Po, po_rm, po_word_new, po_note_new, STATE_SECRET, STATE_ACTIVE, po_state_set
from model.po_pic import pic_list, pic_list_edit, mc_pic_id_list
from model.zsite import Zsite

from model.event import Event, event_feedback_new, CID_EVENT_FEEDBACK

@urlmap('/event/feedback/(\d+)')
def EventFeedback(LoginBase):
    def get(self, event_id):
        event = Event.get(event_id)
        introduction_po = Po.where('cid=%s and rid=%s', CID_EVENT_INTRODUCTION, event_id)[0]
        feedback_po = Po.where('cid=%s and rid=%s', CID_EVENT_FEEDBACK, event_id)[0]
        if event.zsite_id == self.current_user_id and not feedback_po:
            self.template = '/ctrl/me/po/po.htm'
            self.render()

    def post(self, event_id):
        event = Event.get(event_id)
        current_user_id = self.current_user_id
        if event.zsite_id == current_user_id:
            name = self.get_argument('name', None)
            txt = self.get_argument('txt', None)
            event_feedback_new(event_id, current_user_id, name, txt)






