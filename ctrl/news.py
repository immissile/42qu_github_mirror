#!/usr/bin/env python
#coding:utf-8

import _handler
from zweb._urlmap import urlmap
from model.mblog import mblog_word_new

@urlmap("/news")
class News(_handler.LoginBase):
    def get(self):
        return self.render()

