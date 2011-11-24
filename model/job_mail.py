#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM
from user_mail import mail_by_user_id
from model.verify import verify_mail_new, CID_VERIFY_COM_HR



JOB_MAIL_STATE_VERIFY = 10
JOB_MAIL_STATE_VERIFIED = 20

class JobMail(Model):
    pass


def job_mail_new_with_verify_mail(zsite, user_id, mail):
    zsite_id = zsite.id
    mail = mail.strip().lower()

    jm = job_mail_new(zsite_id, mail)

    if mail == mail_by_user_id(user_id):
        jm.state = JOB_MAIL_STATE_VERIFIED
        jm.save()
    else:
        verify_mail_new(zsite_id, zsite.name, mail, CID_VERIFY_COM_HR)


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

        mc_flush(zsite_id, department_id)

    return jm

def mc_flush(zsite_id, department_id):
    key = "%s_%s"%(zsite_id,department_id)
    mc_job_mail_by_com_id.delete(key)
    mc_job_mail_if_exist.delete(key)


@mc_job_mail_by_com_id("{id}_{department_id}")
def job_mail_by_com_id(id, department_id=0):
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


if __name__ == "__main__":
    zsite_id = 10163143
    department_id = 0 
    jm = JobMail.get(zsite_id=zsite_id,department_id=department_id)
    print jm.mail
    mc_flush(zsite_id, department_id)
    print job_mail_if_exist(zsite_id)
