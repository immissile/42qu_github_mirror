#!/usr/bin/dev python
# -*- coding: utf-8 -*-
from _handler import LoginBase
from ctrl._urlmap.me import urlmap
from model import reply
from model.cid import CID_WORD, CID_NOTE, CID_QUESTION, CID_ANSWER
from model.po import Po, po_rm, po_word_new, po_note_new, STATE_SECRET, STATE_ACTIVE, po_state_set
from model.po_pic import pic_list, pic_list_edit, mc_pic_id_list
from model.zsite import Zsite
from model.notice import notice_new

from model.event import Event, EventUser, event_feedback_new, CID_EVENT_FEEDBACK, CID_EVENT_INTRODUCTION, CID_EVENT_USER_SATISFACTION, CID_EVENT_USER_GENERAL, CID_EVENT_USER_FEEDBACK
from zkit.jsdict import JsDict

@urlmap('/event/feedback/reply/(\d+)')
class EventFeedback(LoginBase):
    def post(self, event_id):
        event = Event.get(event_id)
        current_user = self.current_user
        current_user_id = self.current_user_id
        event_user = EventUser.where('user_id=%s and event_id=%s', current_user_id, event_id)[0]
        satisfaction = self.get_argument('satisfaction', None)
        txt = self.get_argument('txt', None)
        if txt:
            feedback_po = event.feedback_po()
            feedback_po.reply_new(current_user, txt, feedback_po.state)
            notice_new(current_user_id, event.zsite_id, CID_EVENT_USER_FEEDBACK, event_id)
        if event_user.state != CID_EVENT_USER_SATISFACTION and event_user.state != CID_EVENT_USER_GENERAL:
            if satisfaction=='on':
                event_user.state = CID_EVENT_USER_SATISFACTION
            else:
                event_user.state = CID_EVENT_USER_GENERAL
            event_user.save()
        self.redirect(feedback_po.link)
                








