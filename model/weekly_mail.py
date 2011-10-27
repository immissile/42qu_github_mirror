#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel

class WeeklyMail(Model):
    pass

def weekly_mail_new(title, txt, state=1):
    return WeeklyMail(
        title=title,
        txt=txt,
        state=state
    ).save()

def weekly_mail_total():
    return WeeklyMail.count()

def weekly_mail_list_limit(limit, offset):
    wm_list = WeeklyMail.raw_sql('select id, title, txt, state from weekly_mail order by id desc limit %s offset %s', limit, offset).fetchall()
    return wm_list

def weekly_mail_rm(id):
    WeeklyMail.where(id=id).delete()

def weekly_mail_update(id, title, txt, state):
    WeeklyMail.raw_sql('update weekly_mail set title=%s,txt=%s,state=%s where id=%s', title, txt, state, id)

if __name__ == '__main__':
    print dir(WeeklyMail)

