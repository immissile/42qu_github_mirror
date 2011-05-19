#!/usr/bin/env python
#coding:utf-8


import _handler
from zweb._urlmap import urlmap

@urlmap("/cout/note")
class Note(_handler.Base):
    def get(self):
        return self.render()

@urlmap("/cout/word")
class Word(_handler.Base):
    def get(self):
        return self.render()

