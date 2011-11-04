#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM

class JobPlace(McModel):
    pass

class JobType(McModel):
    pass

def job_place_new(com_id,pid,name):
    jp = JobPlace(com_id=com_id)
    jp.pid = pid
    jp.name = name
    jp.save()
    return jp

def job_type_new(job_id,type_id):
    jtn = JobType(job_id=job_id,type_id=type_id)
    jtn.save()
    return jtn
