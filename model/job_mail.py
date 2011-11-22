#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM

STATE_VERIFY = 1
STATE_VERIFIED = 2

class JobMail(McModel):
    pass

def get_job_mail(zsite_id):
    jm = JobMail.get(zsite_id=zsite_id)
    if jm:
        return jm.mail

def get_job_mail_state(zsite_id):
    jm = JobMail.get(zsite_id=zsite_id)
    if jm:
        return jm.state
def job_mail_new(zsite_id,mail,department_id=0,state=STATE_VERIFY):
    jm = JobMail.get_or_create(zsite_id=zsite_id)
    jm.mail = mail
    jm.department_id=department_id
    jm.state = state
    jm.save()
    return jm

def job_mail_by_com_id(com_id):
    jm = JobMail.get(zsite_id=com_id)
    if jm and jm.state >= STATE_VERIFIED:
        return jm.mail
