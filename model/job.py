#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McNum, McCacheA, McCacheM, McCacheA
from zkit.job import JOBKIND2CN
from zsite_com import pid_by_com_id
from zkit.attrcache import attrcache

mc_job_type_by_job_id = McCacheA('JobTypeByJobId:%s')
mc_job_kind_by_job_id = McCacheA('JobKindByJobId:%s')
mc_com_job_id_list_by_com_id_state = McCacheA('ComJobIdListByComIdState:%s')

JOBTYPE = (
    (1, '兼职'),
    (2, '实习生'),
    (3, '全职'),
    (4, '合伙人'),
)

JOB_ACTIVE = 5
JOB_CLOSE = 3
JOB_RM = 0

JOB_STATE = (
    JOB_ACTIVE, JOB_CLOSE, JOB_RM
)

SALARY_TYPE = (
    (1, '月薪'),
    (2, '年薪')
)
SALARY_TYPE2CN = dict(SALARY_TYPE)
JOBTYPE2CN = dict(JOBTYPE)

class ComJobNeeds(McModel):
    pass

class ComJob(McModel):
    @attrcache
    def job_department_list(self):
        return ComDepartment.where(com_id=self.id)

    @attrcache
    def needs(self):
        return ComJobNeeds.mc_get(self.id)

class JobPid(McModel):
    pass

class JobType(McModel):
    pass

class JobPidDefault(McModel):
    pass

class JobKind(McModel):
    pass


class ComDepartment(McModel):
    pass


def com_department_edit(id, name):
    cd = ComDepartment.get_or_create(id=id)
    cd.name = name
    cd.save()

def com_department_new(com_id, name):
    cd = ComDepartment(com_id=com_id, name=name)
    cd.save()
    return cd

def com_department_rm_by_id(id):
    return ComDepartment.where(id=id).delete()



def com_department_by_com_id(com_id):
    return ComDepartment.where(com_id=com_id)



@mc_job_kind_by_job_id('{id}')
def job_kind_by_job_id(id):
    return JobKind.where(job_id=id).col_list(col='kind_id')

def job_kind_set(id, kind_list):
    id_set_old = set(job_kind_by_job_id(id))
    id_set_new = set([
        i for i in map(int, kind_list) if i in JOBKIND2CN
        ])
    for kind_id in (id_set_old - id_set_new):
        JobKind.where(job_id=id, kind_id=kind_id).delete()

    for kind_id in (id_set_new - id_set_old):
        jkn = JobKind.get_or_create(job_id=id, kind_id=kind_id)
        jkn.save()
    mc_job_kind_by_job_id.delete(id)

@mc_job_type_by_job_id('{id}')
def job_type_by_job_id(id):
    return JobType.where(job_id=id).col_list(col='type_id')

def job_type_set(id, type_list):
    id_set_old = set(job_type_by_job_id(id))
    id_set_new = set([
        i for i in map(int, type_list) if i in JOBTYPE2CN
    ])

    for type_id in (id_set_old - id_set_new):
        JobType.where(job_id=id, type_id=type_id).delete()

    for type_id in (id_set_new - id_set_old):
        jtn = JobType.get_or_create(job_id=id, type_id=type_id)
        jtn.save()

    mc_job_type_by_job_id.delete(id)

def _job_pid_default_by_com_id(com_id):
    return list(JobPidDefault.where(com_id=com_id))

def job_pid_default_by_com_id(com_id):
    p = _job_pid_default_by_com_id(com_id)
    if not p:
        p = pid_by_com_id(com_id)
    return p

def job_pid_new(job_id, com_pid):
    jp = JobPid.get_or_create(job_id=job_id, pid=com_pid)
    jp.save()
    return jp

def job_pid_default_new(com_id, pid):
    jp = JobPidDefault.get_or_create(com_id=com_id, pid=pid)
    jp.save()
    return jp

def job_kind_new(job_id, kind_id):
    jt = JobKind(job_id=job_id, kind_id=kind_id)
    jt.save()
    return jt

def job_pid_by_job_id(job_id):
    return JobPid.where(job_id=job_id).col_list(col='pid')



def job_new(
        com_id, department_id,
        title, create_time, salary_from, salary_to, salary_type, end_time,
        quota,
        txt, require, stock_option, welfare, priority,
        pids,
        job_type,
        kinds,
        job=None
    ):
    if not job:
        job = ComJob(
            com_id=com_id,
        )
    job.department_id = department_id
    job.title = title
    job.create_time = create_time
    job.salary_from = salary_from
    job.salary_to = salary_to
    job.salary_type = salary_type
    job.end_time = end_time
    job.quota = quota
    job.state = JOB_ACTIVE
    job.save()

    id = job.id
    cjn = ComJobNeeds.get_or_create(id=id)

    cjn.stock_option = stock_option
    cjn.welfare = welfare
    cjn.txt = txt
    cjn.priority = priority
    cjn.require = require
    cjn.save()

    com_id = job.com_id
    if isinstance(pids, list):
        for pid in pids:
            job_pid_default_new(com_id, pid)
            job_pid_new(id, pid)
    else:
        pid = pids
        job_pid_default_new(com_id, pid)
        job_pid_new(id, pid)

    job_type_set(id, job_type)
    job_kind_set(id, kinds)
    mc_flush(com_id)
    return job



def com_job_by_com_id(com_id):
    return com_job_by_com_id_state(com_id, JOB_ACTIVE)

def com_job_by_com_id_state(com_id, state):
    return ComJob.mc_get_list(com_job_id_list_by_com_id_state(com_id, state))


@mc_com_job_id_list_by_com_id_state('{com_id}_{state}')
def com_job_id_list_by_com_id_state(com_id, state):
    return ComJob.where(state=state, com_id=com_id).col_list(col='id')

def com_job_close(id, com_id):
    job = ComJob.mc_get(id)
    if job and job.com_id == com_id:
        if job.state == JOB_ACTIVE:
            job.state = JOB_CLOSE
        elif job.state == JOB_CLOSE:
            job.state == JOB_RM
        job.save()
        mc_flush(com_id)

def mc_flush(com_id):
    for state in JOB_STATE:
        mc_com_job_id_list_by_com_id_state.delete('%s_%s'%(com_id, state))

if __name__ == '__main__':
    from zsite import Zsite
    from zsite_com import ZsiteCom
    from cid import CID_COM
    from zsite_show import zsite_show_list
    from zsite_member import zsite_member_admin_list
    from user_mail import mail_by_user_id
    #job_type_set(25, [2,3225])
    com0, com1, com2, com3 = set(), set(), set(), set()
    for i in ComJob.where():
        com0.add(i.com_id)
    com3 = set([i.id for i in zsite_show_list(CID_COM)])
    #print com3
    for i in Zsite.where(cid=CID_COM):
        com1.add(i.id)
    for i in ZsiteCom.where('video_id != %s', 0):
        com2.add(i.id)
    for i in com1-com3:
        c =  ZsiteCom.mc_get(i) 
        z = Zsite.mc_get(i)
        print '---------'
        print '公司名:',z.name,
        print 'http:%s'%z.link
        print '公司愿望:',c.hope
        print '公司钱:',c.money,
        print '公司文化:',c.culture,
        print '公司团队:',c.team,
        print '公司视频:',c.video_id,
        print '公司电话:',c.phone
    #print len(com0-com2-com3)
    #print';'.join( [mail_by_user_id(zsite_member_admin_list(i)[0].id) for i in com0-com2-com3])
    #print len(com0), len(com1), len(com2), len(com3), len(com0-com2-com3)
