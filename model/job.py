#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM

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
    jt = JobType(job_id=job_id,kind_id=kind_id)
    jt.save()
    return jt
