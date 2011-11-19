#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM
from job import JobType, JobPlace
from zkit.attrcache import attrcache
from cid import CID_COM_PIC
from zkit.pic import pic_fit_width_cut_height_if_large
from fs import fs_set_jpg, fs_url_jpg
from pic import pic_new, pic_save

JOB_ACTIVE = 5
JOB_CLOSE = 4
JOB_DEL = 3


JOBSALARY2CN = {
        1:'月薪',
        2:'年薪'
        }



class ZsiteCom(McModel):
    pass

class ComJob(McModel):
    @attrcache
    def job_department_list(self):
        return ComDepartment.where(com_id=self.id)

    @attrcache
    def needs(self):
        return ComJobNeeds.mc_get(self.id)

def com_pic_new(com_id,pic):
    pic_id = pic_new(CID_COM_PIC,com_id)
    pic_save(pic_id,pic)
    p1 = pic_fit_width_cut_height_if_large(pic,357)
    fs_set_jpg('357',pic_id,p1)
    return pic_id

def zsite_com_new(com_id,hope,money,culture,team,cover_id,video_cid):
    zsite_com = ZsiteCom.get_or_create(id=com_id)
    zsite_com.hope=hope
    zsite_com.money=money
    zsite_com.culture = culture
    zsite_com.cover_id = cover_id
    zsite_com.team = team
    zsite_com.video_cid = video_cid
    zsite_com.save()

def com_job_by_com_id(com_id):
    return ComJob.where(com_id=com_id)

def com_job_by_state_com_id(com_id,state):
    return ComJob.where(state=state,com_id=com_id)

def com_job_by_department_and_com(department_id,com_id):
    return ComJob.where(department_id=department_id,com_id=com_id,state=JOB_ACTIVE)

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

def com_job_new(com_id,department_id,title,txt,create_time,salary_up,salary_down,salary_type,end_time,people_num,state=JOB_ACTIVE):
    cj = ComJob(com_id=com_id,department_id=department_id,title=title,txt=txt,create_time=create_time,salary_up=salary_up,salary_down=salary_down,salary_type=salary_type,end_time=end_time,people_num=people_num)
    cj.state = state
    cj.save()
    return cj

def com_job_needs_new(job_id,requires,stock_option,welfare,priority):
    cjn = ComJobNeeds(id=job_id)
    cjn.stock_option=stock_option
    cjn.welfare=welfare
    cjn.priority = priority
    cjn.requires = requires
    cjn.save()
    return cjn


def com_department_by_com_id(com_id):
    return ComDepartment.where(com_id=com_id)

