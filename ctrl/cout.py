#!/usr/bin/env python
#coding:utf-8

import _handler
from zweb._urlmap import urlmap
from model.mblog import mblog_word_new

@urlmap("/cout/note")
class Note(_handler.LoginBase):
    def get(self):
        return self.render()

@urlmap("/cout/word")
class Word(_handler.LoginBase):
    def post(self):
        current_user = self.current_user
        txt = self.get_argument('txt','')
        if txt.strip():
            mblog_word_new(current_user.id, txt)
        return self.redirect("/news")

