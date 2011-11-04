#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ctrl.zsite._handler import ZsiteBase, LoginBase, XsrfGetBase
from ctrl._urlmap.zsite import urlmap
from model.job_mail import get_job_mail_state, job_mail_new, STATE_VERIFIED
from model.zsite import Zsite
from model.verify import verify_mail_new, CID_VERIFY_COM
from model.zsite_com import get_zsite_com
from zkit.jobs import JOB_PROF 


@urlmap('/job/new')
class JobNew(ZsiteBase):
    def get(self):
        if get_job_mail_state(self.zsite_id) == STATE_VERIFIED:
            com_place_list = get_zsite_com(self.zsite_id)
            print com_place_list,self.zsite_id,'!!!!!!!!!'
            return self.render(com_place_list=com_place_list,job_prof=JOB_PROF)
            #self.finish({'zsite_id':self.zsite_id,'usr_id':self.current_user_id})
        else:
            return self.redirect('/job/mail')


    def post(self):
        
        self.finish('/'.join(dir(self)))

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

@urlmap('/mail/verify')
class MailVerify(ZsiteBase):
    def get(self):
        self.render(zsite_id = self.zsite_id)
