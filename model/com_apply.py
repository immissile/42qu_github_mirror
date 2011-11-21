#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM
from mail import rendermail
from model.days import today_seconds


STATE_APPLY_ACCEPT = 4
STATE_APPLY_MAILED = 3
STATE_APPLY = 2
STATE_DEL = 1

class ComApply(McModel):
    pass


def com_apply_list(com_id,state):
    return ComApply.where(com_id=com_id,state=state)


def com_apply_new(user_id,com_id):
    ca = ComApply.get_or_create(com_id=com_id,user_id=user_id)
    ca.state = STATE_APPLY
    ca.create_time = today_seconds()
    ca.save()
    #admin_id_list = admin_id_list_by_zsite_id(com_id)
    #rendermail(
    #        '/mail/notice/com_apply.txt',
    #        mail_by_user_id(user_id),
    #        user = Zsite.mc_get(user_id),
    #        com = Zsite.mc_get(com_id)
    #        )

def com_apply_rm(user_id,com_id,admin_id):
    ca = ComApply.get(user_id=user_id,com_id=com_id)
    if ca:
        ca.state = STATE_DEL
        ca.admin_id = admin_id
        ca.create_time = today_seconds()
        ca.save()


