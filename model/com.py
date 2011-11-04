#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM
from job import JobType, JobPlace
from zkit.attrcache import attrcache


class ComJob(McModel):
    @attrcache
    def job_department_list(self):
        return ComDepartment.where(com_id=self.id)

    @property
    def com_job_needs(self):
        return ComJobNeeds.mc_get(self.id)


class ComDepartment(McModel):
    pass

class ComJobNeeds(McModel):
    pass

def job_place_list(self):
    return JobPlace.where(com_id=self.id)

def com_department_edit(id,name):
    cd = ComDepartment.get_or_create(id=id)
    cd.name=name
    cd.save()

def com_department_new(com_id,name):
    cd = ComDepartment(com_id=com_id,name=name)
    cd.save()
    return cd

def com_department_rm_by_id(id):
    return ComDepartment.where(id=id).delete()

def com_job_new(com_id,comdepartment_id,title,jd):
    cj = ComJob(com_id=com_id,department_id=comdepartment_id)
    cj.title=title
    cj.jd = jd
    cj.save()
    return cj.id

def com_job_needs_new(job_id,acquirs,stock_option,welfare,priority):
    cjn = ComJobNeeds(job_id=job_id,salary=salary,salary_type=salary_type)
    cjn.stock_option=stock_option
    cjn.welfare=welfare
    cjn.desirable=desirable
    cjn.time_limit=time_limit
    cjn.job_type=job_type
    cjn.save()
    return cjn


def com_department_by_com_id(com_id):
    return ComDepartment.where(com_id=com_id)

