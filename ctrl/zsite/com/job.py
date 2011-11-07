#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ctrl.zsite._handler import ZsiteBase, LoginBase, XsrfGetBase
from ctrl._urlmap.zsite import urlmap
from model.job_mail import get_job_mail_state, job_mail_new, STATE_VERIFIED
from model.zsite import Zsite
from model.verify import verify_mail_new, CID_VERIFY_COM
from model.zsite_com import get_zsite_com
from zkit.job import JOB_KIND 
from model.com import com_department_new, com_job_new, com_job_needs_new, com_department_by_com_id, com_department_rm_by_id, com_department_edit
import json
from model.job import job_type_new, job_pid_new, job_place_new, job_pid_by_com_id, job_kind_new
from model.days import today_days

@urlmap('/job/new')
class JobNew(ZsiteBase):
    def get(self):
        if get_job_mail_state(self.zsite_id) == STATE_VERIFIED:
            com_place_list1 = get_zsite_com(self.zsite_id)
            com_place_list2 = job_pid_by_com_id(self.zsite_id)
            com_place_list = com_place_list2 or com_place_list1
            job_kind = json.dumps(JOB_KIND)
            com_department_list = com_department_by_com_id(self.zsite_id)
            return self.render(com_place_list=com_place_list,job_prof=job_kind, com_department_list=com_department_list)
        else:
            return self.redirect('/job/mail')


    def post(self):
        department_id = self.get_argument('depart',None)
        title = self.get_argument('title',None)
        kinds = self.get_argument('prof',None)
        stock_option = self.get_argument('share',None)
        priority = self.get_argument('more',None)
        job_type = self.get_argument('type',None)
        acquires = self.get_argument('requ',None)
        job_description = self.get_argument('desc',None)
        welfare = self.get_argument('other',None)
        salary_up  = self.get_argument('salary1',None)
        salary_down = self.get_argument('salary2',None)
        salary_type = self.get_argument('sal_type',None)
        dead_line = self.get_argument('deadline',None)
        pids = self.get_argument('pid',None)
        
       
        if department_id and title and job_description and dead_line and salary_up and salary_type and salary_down:
            cj = com_job_new(
                    self.zsite_id,
                    department_id,
                    title,
                    job_description,
                    today_days(),
                    salary_up,
                    salary_down,
                    salary_type,
                    int(dead_line)*30+today_days())
        
        
        if acquires and stock_option and welfare and priority and cj:
            cjn = com_job_needs_new(cj.id,acquires,stock_option,welfare,priority)
        
        
        if pids and cjn:
            if isinstance(pids,list):
                for pid in pids:
                    job_pid_new(self.zsite_id,pid)
                    job_place_new(cj.id,pid)
            else:
                pid = pids
                job_pid_new(self.zsite_id,pid)
                job_place_new(cj.id,pid)
        
        
        if job_type and cj:
            job_type_new(cj.id,job_type)
        
        
        if kinds and cj:
            kinds = kinds.split('-')[:-1]
            for kind in kinds:
                job_kind_new(cj.id,kind)
        
        self.finish(str(cj.id))
                
        

@urlmap('/job/department/rm')
class JobDepartmentRm(ZsiteBase):
    def post(self):
        id = self.get_argument('id',None)
        if id:
            com_department_rm_by_id(id)
            self.finish({'result':True})

@urlmap('/job/depart/add')
class JobDepartAdd(ZsiteBase):
    def post(self):
        txt = self.get_argument('txt',None)
        cd = com_department_new(self.zsite_id,txt)
        self.finish(str(cd.id))

@urlmap('/job/depart/write')
class JobDepartWrite(ZsiteBase):
    def post(self):
        id = self.get_arguments('pop_de_id',None)
        name = self.get_arguments('pop_de_name',None)
        kv = zip(id,name)
        print kv,'!!!!!!!!'
        for k,v in kv:
            com_department_edit(k,v)
        self.finish({'result':True})

@urlmap('/job/mail')
class JobMail(ZsiteBase):
    def get(self):
        self.render(current_user_id=self.current_user_id)

    def post(self):
        hr_mail = self.get_argument('hr_mail',None)
        zsite_id = self.zsite_id
        zsite = Zsite.mc_get(zsite_id)
        if hr_mail:
            job_mail_new(zsite_id,hr_mail)
            verify_mail_new(zsite_id,zsite.name,hr_mail,CID_VERIFY_COM)
            return self.redirect('/mail/verify')
        else:
            return self.get()

@urlmap('/mail/verify')
class MailVerify(ZsiteBase):
    def get(self):
        self.render()
