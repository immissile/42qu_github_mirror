#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM
from job import JobType, JobPlace

class ComJob(McModel):
    @attrcache
    def job_department_list(self):
        return ComDepartment.where(com_id=self.id)

    @property
    def com_job_needs(self):
        return ComJobNeeds.mc_get(com_id=self.id)

    def job_place_list(self):
        return JobPlace.where(com_id=self.id)

class ComDepartment(McModel):
    pass

class ComJobNeeds(McModel):
    pass


def new_com_department(com_id,name):
    cd = ComDepartment(com_id=com_id,name=name)
    cd.save()
    return cd

def new_com_job(com_id,comdepartment_id,title,jd):
    cj = ComJob(com_id=com_id,department_id=comdepartment_id)
    cj.title=title
    cj.jd = jd
    cj.save()
    return cj.id

def new_com_job_needs(job_id,acquirs,salary,salary_type,stock_option,welfare,desirable,time_limit,job_type):
    cjn = ComJobNeeds(job_id=job_id,salary=salary,salary_type=salary_type)
    cjn.stock_option=stock_option
    cjn.welfare=welfare
    cjn.desirable=desirable
    cjn.time_limit=time_limit
    cjn.job_type=job_type
    cjn.save()
    return cjn


def get_com_department(com_id):
    return ComDepartment.where(com_id=com_id)

