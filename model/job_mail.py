#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM



JOB_MAIL_STATE_VERIFY = 10
JOB_MAIL_STATE_VERIFIED = 20

class JobMail(Model):
    pass


mc_job_mail_by_com_id = McCache("JobMailByComId:%s")
mc_job_mail_if_exist = McCache("JobMailIfExist:%s")

def job_mail_new(zsite_id, mail, department_id=0, state=JOB_MAIL_STATE_VERIFY):
    mail = mail.strip().lower()
    if mail:
        if mail == job_mail_by_com_id(id, department_id):
            return
        jm = JobMail.get_or_create(zsite_id=zsite_id,department_id=department_id)
        jm.mail = mail
        jm.department_id = department_id
        jm.state = state
        jm.save()

        mc_flush(zsite_id)

    return jm

def mc_flush(zsite_id, department_id):
    key = "%s_%s"%(zsite_id,department_id)
    mc_job_mail_by_com_id.delete(key)
    mc_job_mail_if_exist.delete(department_id)

@mc_job_mail_by_com_id("{id}_{department_id}")
def job_mail_by_com_id(id, department_id):
    jm = JobMail.get(zsite_id=id,department_id=department_id)
    if jm and jm.state >= JOB_MAIL_STATE_VERIFIED:
        return jm.mail
    return ''


@mc_job_mail_if_exist("{id}_{department_id}")
def job_mail_if_exist(id,department_id=0):
    jm = JobMail.get(zsite_id=id,department_id=department_id)
    if jm:
        return jm.mail
    return ''

def job_mail_verifyed(id,department_id=0):
    jm = JobMail.get(zsite_id=id,department_id=department_id)
    if jm:
        jm.state = JOB_MAIL_STATE_VERIFIED
        jm.save()
        mc_flush(id,department_id)

