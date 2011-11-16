#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM

JOBTYPE2CN={
        1:'兼职',
        2:'实习生',
        3:'全职',
        4:'合伙人',
        }

class JobPlace(McModel):
    pass

class JobType(McModel):
    pass

class JobPid(McModel):
    pass

class JobKind(McModel):
    pass

def job_place_new(job_id,com_pid):
    jp = JobPlace.get_or_create(job_id=job_id,pid=com_pid)
    jp.save()
    return jp

def job_type_new(job_id,type_id):
    jtn = JobType(job_id=job_id,type_id=type_id)
    jtn.save()
    return jtn

def job_pid_by_com_id(com_id):
    jp = JobPid.where(com_id=com_id)
    return JobPid.where(com_id=com_id)

def job_pid_new(com_id,pid):
    jp = JobPid.get_or_create(com_id=com_id,pid=pid)
    jp.save()
    return jp

def job_kind_new(job_id,kind_id):
    jt = JobKind(job_id=job_id,kind_id=kind_id)
    jt.save()
    return jt

def job_place_by_job_id(job_id):
    return JobPlace.where(job_id=job_id).col_list(col='pid')

def job_type_by_job_id(job_id):
    return JobType.where(job_id=job_id).col_list(col='type_id')

def job_kind_by_job_id(job_id):
    return JobKind.where(job_id=job_id).col_list(col='kin_id')
