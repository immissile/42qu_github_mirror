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


@urlmap('/job/new')
class JobNew(ZsiteBase):
    def get(self):
        if get_job_mail_state(self.zsite_id) == STATE_VERIFIED:
            com_place_list = get_zsite_com(self.zsite_id)
            print com_place_list,self.zsite_id,'!!!!!!!!!'
            job_prof = json.dumps(JOB_KIND)
            com_department_list = com_department_by_com_id(self.zsite_id)
            return self.render(com_place_list=com_place_list,job_prof=job_prof, com_department_list=com_department_list)
            #self.finish({'zsite_id':self.zsite_id,'usr_id':self.current_user_id})
        else:
            return self.redirect('/job/mail')


    def post(self):
        depart = self.get_argument('depart',None)
        title = self.get_argument('title',None)
        prof = self.get_argument('prof',None)
        option_share = self.get_argument('share',None)
        acquires = self.get_argument('more',None)
        job_type = self.get_argument('type',None)
        requ = self.get_argument('requ',None)
        job_descripe = self.get_argument('desc',None)
        desirable = self.get_argument('other',None)
        salary = self.get_argument('salary1-salary2',None)
        salary_type = self.get_argument('salary_type',None)
        print depart ,'depart'
        print desirable,'desirable'
        print job_descripe,'desc'
        print acquires,'acquires'
        print requ,'requ'
        print job_type,'job_type'
        print salary_type,'salary_type'
        print salary,'salary'
        print title,'title'
        print prof,'prof'
        print option_share,'option_share'
                
        
        self.finish('/'.join(dir(self)))

@urlmap('/job/department/rm')
class JobDepartmentRm(ZsiteBase):
    def post(self):
        id = self.get_argument(id)
        if id:
            com_department_rm_by_id(id)
            self.finsih({'result':True})

@urlmap('/job/depart/add')
class JobDepartAdd(ZsiteBase):
    def post(self):
        txt = self.get_argument('txt')
        cd = com_department_new(self.zsite_id,txt)
        self.finsih(cd.id)

@urlmap('/job/depart/write')
class JobDepartWrite(ZsiteBase):
    def post(self):
        kv = self.get_argument('kv',None)
        for k,v in kv:
            com_department_edit(k,v)
            self.finsih({'result':True})

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
