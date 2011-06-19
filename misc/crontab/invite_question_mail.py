#!/usr/bin/env python
# -*- coding: utf-8 -*-
import init_env
from zkit.single_process import single_process
from model.kv_misc import kv_int, KV_INVITE_QUESTION_POS
from midel.cid import CID_INVITE_QUESTION
from model.notice import Notice, invite_question_mail

@single_process
def invite_question():
    prev_pos = kv_int.get(KV_INVITE_QUESTION_POS)
    c = Notice.raw_sql('select max(id) from notice')
    pos = c.fetchone()[0]
    if pos > prev_pos:
        for i in Notice.where(cid=CID_INVITE_QUESTION).where('%s<id<=%s', prev_pos, pos):
            invite_question_mail(i)
        kv_int.set(KV_INVITE_QUESTION_POS, pos)

if __name__ == '__main__':
    invite_question()
