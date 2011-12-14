#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM
from user_mail import mail_by_user_id
from model.verify import verify_mail_new, CID_VERIFY_COM_HR, verify_rm



JOB_MAIL_STATE_VERIFY = 10
JOB_MAIL_STATE_VERIFIED = 20

mc_job_mail_by_com_id = McCache('JobMailByComId:%s')
mc_job_mail_if_exist = McCache('JobMailIfExist:%s')

class JobMail(Model):
    pass


def job_mail_new_with_verify_mail(zsite, user_id, mail):
    zsite_id = zsite.id
    mail = mail.strip().lower()

    if job_mail_if_exist(zsite_id) != mail:
        verify_rm(zsite_id, CID_VERIFY_COM_HR)

    jm = job_mail_new(zsite_id, mail)

    if mail == mail_by_user_id(user_id) or mail == job_mail_by_com_id(zsite_id) :
        jm.state = JOB_MAIL_STATE_VERIFIED
        jm.save()
    else:
        verify_mail_new(zsite_id, zsite.name, mail, CID_VERIFY_COM_HR)


def job_mail_new(zsite_id, mail, school_department=0, state=JOB_MAIL_STATE_VERIFY):
    mail = mail.strip().lower()
    if mail:
        job = JobMail.get_or_create(zsite_id=zsite_id, school_department=school_department)

        if job.mail == mail and state == JOB_MAIL_STATE_VERIFY and job.state == JOB_MAIL_STATE_VERIFIED:
            state = JOB_MAIL_STATE_VERIFIED

        job.state = state
        job.mail = mail
        job.save()

        mc_flush(zsite_id, school_department)

        return job

def mc_flush(zsite_id, school_department):
    key = '%s_%s'%(zsite_id, school_department)
    mc_job_mail_by_com_id.delete(key)
    mc_job_mail_if_exist.delete(key)


@mc_job_mail_by_com_id('{id}_{school_department}')
def job_mail_by_com_id(id, school_department=0):
    jm = JobMail.get(zsite_id=id, school_department=school_department)
    if jm and jm.state >= JOB_MAIL_STATE_VERIFIED:
        return jm.mail
    return ''


@mc_job_mail_if_exist('{id}_{school_department}')
def job_mail_if_exist(id, school_department=0):
    jm = JobMail.get(zsite_id=id, school_department=school_department)
    if jm:
        return jm.mail
    return ''

def job_mail_verifyed(id, school_department=0):
    jm = JobMail.get(zsite_id=id, school_department=school_department)
    if jm:
        jm.state = JOB_MAIL_STATE_VERIFIED
        jm.save()
        mc_flush(id, school_department)


if __name__ == '__main__':
    for i in JobMail.where(mail="dreamerunion@126.com"):
        print i
        job_mail_verifyed(i.zsite_id)
   # zsite_id = 10163143
   # school_department = 0
   # jm = JobMail.get(zsite_id=zsite_id, school_department=school_department)
   # print jm.mail
   # mc_flush(zsite_id, school_department)
   # print job_mail_if_exist(zsite_id)
