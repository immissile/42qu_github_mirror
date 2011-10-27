#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel

class Weekly_mail(McModel):
    pass

def weekly_mail_new(title, txt, state=1):
    wm = Weekly_mail.get_or_create()
    wm.title = title
    wm.txt = txt
    wm.state = state
    wm.save()
    return wm

def weekly_mail_total():
    return Weekly_mail.count()

def get_weekly_mail_list():
    wm_list = Weekly_mail.raw_sql('select * from weekly_mail order by id desc').fetchall()
    return wm_list

def get_weekly_mail_list_limit(limit=1, offset=10):
    wm_list = Weekly_mail.raw_sql('select * from weekly_mail order by id desc limit %s offset %s', limit, offset).fetchall()
    return wm_list

def weekly_mail_remove(id):
    Weekly_mail.raw_sql('delete from weekly_mail where id = %s', id)

def weekly_mail_update(id,title,txt,state):
    Weekly_mail.raw_sql('update weekly_mail set title=%s,txt=%s,state=%s where id=%s',title,txt,state,id)

if __name__ == "__main__":
    print dir(Weekly_mail)
