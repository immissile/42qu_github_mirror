#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _handler
from zweb._urlmap import urlmap
from model.mblog import mblog_word_new, mblog_note_new, MBLOG_STATE_SECRET, MBLOG_STATE_ACTIVE

@urlmap("/cout/note")
@urlmap("/cout/note/(\d+)")
class Note(_handler.LoginBase):
    def get(self, id=None):
        return self.render()

    def post(self, id=None):
        current_user = self.current_user
        current_user_id = current_user.id
        name = self.get_argument('name', '')
        txt = self.get_argument('txt', '')
        secret = self.get_argument('secret', None)
        if secret:
            state = MBLOG_STATE_SECRET
        else:
            state = MBLOG_STATE_ACTIVE
        m = mblog_note_new(current_user_id, name, txt, state)
        if m:
            return self.redirect("/note/%s"%m.id)


@urlmap("/cout/word")
class Word(_handler.LoginBase):
    def post(self):
        current_user = self.current_user
        txt = self.get_argument('txt', '')
        if txt.strip():
            mblog_word_new(current_user.id, txt)
        return self.redirect("/news")
