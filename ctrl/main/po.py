#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from zweb._urlmap import urlmap
from model.po import po_rm, po_word_new, Po
from model.po_pos import po_pos_get, po_pos_set
from model import reply
from model.zsite import Zsite


@urlmap('/po/(\d+)')
class PoIndex(Base):
    def get(self, id):
        po = Po.mc_get(id)
        if po:
            link = po.link
        else:
            link = "/"
        self.redirect(link)

@urlmap('/po/word')
class Word(LoginBase):
    def post(self):
        current_user = self.current_user
        txt = self.get_argument('txt', '')
        if txt.strip():
            po_word_new(current_user.id, txt)
        return self.redirect('/feed')



