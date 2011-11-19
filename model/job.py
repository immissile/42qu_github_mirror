#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM
from zkit.job import JOBKIND2CN
from zsite_com import pid_by_com_id

mc_job_type_by_job_id = McCacheA("JobTypeByJobId:%s")
mc_job_kind_by_job_id = McCacheA("JobKindByJobId:%s")
JOBTYPE = (
    (1, '兼职'),
    (2, '实习生'),
    (3, '全职'),
    (4, '合伙人'),
)

SALARY_TYPE=(
    (1,'月薪'),
    (2,'年薪')
)
JOBTYPE2CN = dict(JOBTYPE)

class JobPlace(McModel):
    pass

class JobType(McModel):
    pass

class JobPid(McModel):
    pass

class JobKind(McModel):
    pass

def job_place_new(job_id, com_pid):
    jp = JobPlace.get_or_create(job_id=job_id, pid=com_pid)
    jp.save()
    return jp

@mc_job_kind_by_job_id("{id}")
def job_kind_by_job_id(id):
    return JobKind.where(job_id=id).col_list(col='kind_id')

def job_kind_set(id,kind_list):
    id_set_old = set(job_kind_by_job_id(id))
    id_set_new = set([
        i for i in map(int,kind_list) if i in JOBKIND2CN
        ])
    for kind_id in (id_set_old - id_set_new):
        JobKind.where(job_id=id,kind_id=kind_id).delete()

    for kind_id in (id_set_new - id_set_old):
        jkn = JobKind.get_or_create(job_id=id,kind_id=kind_id)
        jkn.save()
    mc_job_kind_by_job_id.delete(id)

@mc_job_type_by_job_id("{id}")
def job_type_by_job_id(id):
    return JobType.where(job_id=id).col_list(col='type_id')

def job_type_set(id, type_list):
    id_set_old = set(job_type_by_job_id(id))
    id_set_new = set([
        i for i in map(int,type_list) if i in JOBTYPE2CN
    ])
    
    for type_id in (id_set_old - id_set_new):
        JobType.where(job_id=id, type_id=type_id).delete()
 
    for type_id in (id_set_new - id_set_old):
        jtn = JobType.get_or_create(job_id=id, type_id=type_id)
        jtn.save() 

    mc_job_type_by_job_id.delete(id)


def job_pid_by_com_id(com_id):
    p = JobPid.where(com_id=com_id)
    if not p:
        p = pid_by_com_id(com_id)
    return p

def job_pid_new(com_id, pid):
    jp = JobPid.get_or_create(com_id=com_id, pid=pid)
    jp.save()
    return jp

def job_kind_new(job_id, kind_id):
    jt = JobKind(job_id=job_id, kind_id=kind_id)
    jt.save()
    return jt

def job_place_by_job_id(job_id):
    return JobPlace.where(job_id=job_id).col_list(col='pid')



if __name__ == "__main__":
    job_type_set(25, [2,3225])
