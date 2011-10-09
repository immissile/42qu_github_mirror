#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McCacheA, McLimitA, McNum

STATE_NEW = 0
STATE_USED = 1

STATE2CN = {
        STATE_NEW : '新建',
        STATE_USED : '已经发送'
        }



class MailPo(McModel):
    pass


def get_tem_total_by_state(state):
    return MailPo.where(state=state).count()


def get_tem_by_state(state, limit=1, offset=10):
    m = MailPo.where(state=state)[offset:limit+offset]
    return m


def new_mail_tem(po_id, state=STATE_NEW):
    MailPo.raw_sql('insert into mail_po (po_id,state) values(%s,%s)', po_id, state)
    return MailPo.where(po_id=po_id).where(state=state)

def rm_tem_by_id(id):
    MailPo.where(id=id).delete()
    return True

