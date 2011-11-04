#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM

class JobPlace(McModel):
    pass

class JobType(McModel):
    pass

class JobPid(McModel):
    pass

def job_place_new(job_id,com_pid):
    jp = JobPlace.get_or_create(job_id=job_id,com_pid=com_pid)
    jp.save()
    return jp

def job_type_new(job_id,type_id):
    jtn = JobType(job_id=job_id,type_id=type_id)
    jtn.save()
    return jtn
