#!/usr/bin/env python
#coding:utf-8


import _handler
from _urlmap import urlmap
from model.po import po_word_new
@urlmap('/po/word')
class Index(_handler.ApiLoginBase):
    def get(self):
        user_id = self.current_user_id
        txt = self.get_argument('txt')
        result = {}
        if txt.strip():
            m = po_word_new(user_id, txt)
            if m:
                result['id'] = m.id
                result['link'] = 'http:%s'%m.link
        self.finish(result)

