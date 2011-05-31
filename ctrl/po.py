#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _handler
from zweb._urlmap import urlmap
from model.po import po_word_new



@urlmap("/po/word")
class Word(_handler.LoginBase):
    def post(self):
        current_user = self.current_user
        txt = self.get_argument('txt', '')
        if txt.strip():
            po_word_new(current_user.id, txt)
        return self.redirect("/feed")
