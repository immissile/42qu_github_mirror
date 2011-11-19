#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ctrl.zsite._handler import ZsiteBase, LoginBase, XsrfGetBase
from ctrl._urlmap.zsite import urlmap
from model.job_mail import get_job_mail_state, job_mail_new, STATE_VERIFIED
from model.zsite import Zsite
from model.verify import verify_mail_new, CID_VERIFY_COM_HR
import json
from model.job import job_type_set, job_pid_default_new, job_pid_new, job_pid_default_by_com_id, job_kind_set, job_kind_by_job_id, job_type_by_job_id, job_pid_by_job_id, job_new, \
ComJob, JOB_ACTIVE, JOB_CLOSE, com_job_by_state_com_id, com_department_new,   com_department_rm_by_id, com_department_edit
from model.days import today_days
from model.zsite_member import zsite_member_can_admin
from _handler import AdminBase
from zkit.errtip import Errtip
from zkit.txt import EMAIL_VALID
from zkit.jsdict import JsDict


def _job_save(self, job=None):
    errtip = Errtip()
    department_id = self.get_argument('depart', None)
    title = self.get_argument('title', None)
    kinds = self.get_argument('kinds', None)
    stock_option = self.get_argument('share', None)
    priority = self.get_argument('more', None)
    job_type = self.get_arguments('type', None)
    require = self.get_argument('require', None)
    txt = self.get_argument('txt', None)
    welfare = self.get_argument('other', None)
    salary_up = self.get_argument('salary1', None)
    salary_down = self.get_argument('salary2', None)
    salary_type = self.get_argument('sal_type', None)
    dead_line = self.get_argument('deadline', None)
    pids = self.get_arguments('addr', None)
    quota = self.get_argument('quota', None)

    if not department_id:
        errtip.department_id = '请选择部门'
    if not title:
        errtip.title = '请输入职位头衔'
    if not kinds:
        errtip.kinds = '请选择行业'
    if not job_type:
        errtip.job_type = '请选择工作种类'
    if not pids:
        errtip.addr = '请选择工作地址'
    if not quota.isdigit():
        errtip.quota = '请设定人数'
    if not (salary_up and salary_down):
        errtip.salary = '必须设定薪水'
    if not(salary_up.isdigit() and salary_down.isdigit()):
        errtip.salary = '请输入正确的薪水'
    if salary_down.isdigit() and salary_up.isdigit() and int(salary_up) > int(salary_down):
        errtip.salary = '最低薪水必须大于最高薪水'
    if not txt:
        errtip.txt = '请填写职位描述'
    if not dead_line:
        errtip.dead_line = '必须选择过期时间'
    if not salary_type:
        errtip.salary_type = '必须选择工资类型'

    if not errtip:
        cj = job_new(
                self.zsite_id,
                department_id,
                title,
                today_days(),
                salary_up,
                salary_down,
                salary_type,
                int(dead_line)+today_days(),
                quota,
                txt,
                require, stock_option, welfare, priority,
                pids,
                job_type,
                kinds.split('-'),
                job
            )

        self.redirect('/job/%s'%cj.id)
    else:
        self.render(
                errtip=errtip,
                title=title,
                stock_option=stock_option,
                kinds=kinds.split('-'),
                priority=priority,
                job_type=job_type,
                require=require,
                txt=txt,
                welfare=welfare,
                salary_type=salary_type,
                salary1=salary_up,
                salary2=salary_down,
                dead_line=dead_line,
                addr=pids,
                quota=quota,
        )



@urlmap('/job/new')
class JobNew(AdminBase):
    def get(self):
        if get_job_mail_state(self.zsite_id) == STATE_VERIFIED:
            return self.render(errtip=Errtip())
        else:
            return self.redirect('/job/mail')

    post = _job_save

@urlmap('/job/edit/(\d+)')
class JobEdit(AdminBase):
    def get(self, id):
        job = ComJob.mc_get(id)
        if job and job.com_id == self.zsite_id:
            needs = job.needs
            self.render(
                errtip=Errtip(),
                title=job.title,
                kinds=job_kind_by_job_id(job.id),
                job_type=job_type_by_job_id(job.id),

                txt=needs.txt,
                stock_option=needs.stock_option,
                priority=needs.priority,
                require=needs.require,
                welfare=needs.welfare,

                salary_type=job.salary_type,
                salary1=job.salary_up,
                salary2=job.salary_down,
                dead_line=90,
                quota=job.quota,
                job=job,
                addr=job_pid_by_job_id(job.id)
            )
        else:
            return self.redirect('/job/admin')

    _job_save = _job_save

    def post(self, id):
        job = ComJob.mc_get(id)
        if job and job.com_id == self.zsite_id:
            self._job_save(job)
        else:
            return self.redirect('/job/admin')

@urlmap('/job/close/(\d+)')
class JobClose(AdminBase):
    def get(self, id):
        job = ComJob.mc_get(id)
        if job:
            job.state = JOB_CLOSE
            job.save()
            return self.redirect('/')

@urlmap('/job/(\d+)')
class JobD(ZsiteBase):
    def get(self, id):
        job = ComJob.mc_get(id)
        if job.state >= JOB_ACTIVE:
            return self.render(job=job, com_id=self.zsite_id, current_user_id=self.current_user_id)
        else:
            self.redirect('/')


@urlmap('/job/department/rm')
class JobDepartmentRm(AdminBase):
    def post(self):
        id = self.get_argument('id', None)
        result = None
        if id:
            com_department_rm_by_id(id)
            result = True
        self.finish({'result':result})

@urlmap('/job/department/add')
class JobDepartmentAdd(AdminBase):
    def post(self):
        txt = self.get_argument('txt', None)
        cd = com_department_new(self.zsite_id, txt)
        self.finish(str(cd.id))

@urlmap('/job/department/write')
class JobDepartmentWrite(AdminBase):
    def post(self):
        id = self.get_arguments('pop_de_id', None)
        name = self.get_arguments('pop_de_name', None)
        kv = zip(id, name)
        result = None
        for k, v in kv:
            com_department_edit(k, v)
            result = True
        self.finish({'result':result})

@urlmap('/job/mail')
class JobMail(AdminBase):
    def get(self):
        err = Errtip()
        self.render(current_user_id=self.current_user_id, errtip=err)

    def post(self):
        hr_mail = self.get_argument('hr_mail', None)
        zsite_id = self.zsite_id
        zsite = Zsite.mc_get(zsite_id)
        if hr_mail and EMAIL_VALID.match(hr_mail):
            job_mail_new(zsite_id, hr_mail)
            verify_mail_new(zsite_id, zsite.name, hr_mail, CID_VERIFY_COM_HR)
            return self.redirect('/mail/verify')
        else:
            err = Errtip()
            err.mail = '邮件格式错误'
            return self.render(errtip=err, current_user_id=self.current_user_id)

@urlmap('/mail/verified')
class MailVerified(AdminBase):
    def get(self):
        zsite_id = self.zsite_id
        zsite = Zsite.mc_get(zsite_id)
        from model.user_mail import mail_by_user_id
        jm = job_mail_new(zsite_id, mail_by_user_id(self.current_user_id))
        verify_mail_new(zsite_id, zsite.name, mail_by_user_id(self.current_user_id), CID_VERIFY_COM_HR)
        jm.state = STATE_VERIFIED
        jm.save()
        self.redirect('/job/new')


@urlmap('/mail/verify')
class MailVerify(AdminBase):
    def get(self):
        self.render()

@urlmap('/job/admin')
@urlmap('/job/admin/(\d+)')
class JobAdmin(AdminBase):
    def get(self, state=JOB_ACTIVE):
        job_list = com_job_by_state_com_id(self.zsite_id, state)
        self.render(job_list=job_list, state=state)

@urlmap('/job/rm/(\d+)')
class JobRm(AdminBase):
    def post(self, state):
        id = self.get_argument('id', None)
        job = ComJob.mc_get(id)
        if job.state == int(state):
            job.state = job.state-1
            job.save()
