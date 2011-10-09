#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McCacheA, McLimitA, McNum

STATE_NEW = 0
STATE_USED = 1

class MailTemplate(McModel):
    pass


def get_tem_total_by_state(state):
    return MailTemplate.where(state=state).count()


def get_tem_by_state(state, limit=1, offset=10):
    return MailTemplate.where(state=state)[limit:limit+offset]

def new_mail_tem(po_id,state=STATE_NEW):
    MailTemplate.raw_sql('insert into mail_template (po_id,state) values(%s,%s)',po_id,state)
    return MailTemplate.where(po_id=po_id).where(state=state)



