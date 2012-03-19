#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ctrl.zsite._handler import ZsiteBase, LoginBase
from ctrl._urlmap.zsite import urlmap
from model.job_mail import  job_mail_new, JOB_MAIL_STATE_VERIFIED, job_mail_by_com_id, job_mail_new_with_verify_mail
from model.zsite import Zsite
from model.job import job_pid_default_new, job_pid_new, job_pid_default_by_com_id, job_kind_set, job_kind_by_job_id, job_type_by_job_id, job_pid_by_job_id, job_new,\
ComJob, JOB_RM, JOB_ACTIVE, JOB_CLOSE, com_job_by_com_id_state, com_department_new, com_department_rm_by_id, com_department_edit, com_job_close
from model.days import today_days
from model.zsite_member import zsite_member_can_admin
from _handler import AdminBase
from zkit.errtip import Errtip
from zkit.txt import EMAIL_VALID
from zkit.jsdict import JsDict
from model.user_mail import mail_by_user_id


def _job_save(self, job=None, add=None):
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
    salary_from = self.get_argument('salary1', None)
    salary_to = self.get_argument('salary2', None)
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
    if not (salary_from and salary_to):
        errtip.salary = '必须设定薪水'
    if not(salary_from.isdigit() and salary_to.isdigit()):
        errtip.salary = '请输入正确的薪水'
    else:
        salary_from = int(salary_from)
        salary_to = int(salary_to)
        if salary_from > salary_to:
            salary_to, salary_from = salary_from, salary_to

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
                salary_from,
                salary_to,
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
        if add:
            return self.redirect('/job/admin')
        elif not job:
            return self.redirect('/job/next')
        else:
            return self.redirect('/job/admin')
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
                salary1=salary_from,
                salary2=salary_to,
                dead_line=dead_line,
                addr=pids,
                quota=quota,
        )



@urlmap('/job/new')
class JobNew(AdminBase):
    def get(self):
        if job_mail_by_com_id(self.zsite_id):
            return self.render(errtip=Errtip())
        else:
            return self.redirect('/job/mail')

    post = _job_save

@urlmap('/job/add')
class JobAdd(AdminBase):
    def get(self):
        if job_mail_by_com_id(self.zsite_id):
            return self.render(errtip=Errtip())
        else:
            return self.redirect('/job/mail')
    _job_save = _job_save

    def post(self):
        self._job_save(add=True)

@urlmap('/job/next')
class JobNext(AdminBase):
    def get(self):
        self.render()


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
                salary1=job.salary_from,
                salary2=job.salary_to,
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
        com_job_close(id, self.zsite_id)
        return self.redirect('/job/admin')



@urlmap('/job/(\d+)')
class JobD(ZsiteBase):
    def get(self, id):
        job = ComJob.mc_get(id)
        if job.state >= JOB_CLOSE:
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
        current_user_id = self.current_user_id
        hr_mail = self.get_argument('hr_mail', '').strip().lower()
        zsite_id = self.zsite_id
        zsite = self.zsite

        errtip = Errtip()
        if hr_mail:
            if not EMAIL_VALID.match(hr_mail):
                errtip.mail = '邮件格式错误'
        else:
            errtip.mail = '请输入邮箱'

        if errtip:
            return self.render(errtip=errtip, current_user_id=current_user_id)
        else:
            job_mail_new_with_verify_mail(zsite, current_user_id, hr_mail)
            return self.redirect('/job/mail/verify')

@urlmap('/job/mail/now')
class MailVerified(AdminBase):
    def get(self):
        admin = self.get_argument('admin', None)
        zsite_id = self.zsite_id
        zsite = Zsite.mc_get(zsite_id)

        jm = job_mail_new(zsite_id, mail_by_user_id(self.current_user_id))
        jm.state = JOB_MAIL_STATE_VERIFIED
        jm.save()
        if admin:
            self.redirect('/job/admin/mail')
        else:
            self.redirect('/job/new')

@urlmap('/job/mail/verify')
class MailVerify(AdminBase):
    def get(self):
        self.render()


@urlmap('/job/admin')
@urlmap('/job/admin/(\d+)')
class JobAdmin(AdminBase):
    def get(self, state=JOB_ACTIVE):
        job_list = com_job_by_com_id_state(self.zsite_id, state)
        self.render(job_list=job_list, state=state)

@urlmap('/job/admin/mail')
class JobAdminMail(AdminBase):
    def get(self):
        errtip = Errtip()
        self.render(
                errtip=errtip
                )

    def post(self):
        hr_mail = self.get_argument('hr_mail', None)
        errtip = Errtip()
        if not EMAIL_VALID.match(hr_mail):
            errtip.hr_mail = '请输入正确的邮箱'
        if not errtip:
            job_mail_new_with_verify_mail(self.zsite, self.current_user_id, hr_mail)
            self.get()
        else:
            self.render(
                errtip=errtip,
                hr_mail=hr_mail,
            )


@urlmap('/job/rm/(\d+)')
class JobRm(AdminBase):
    def post(self, id):
        com_job_close(id, self.zsite_id)
        self.finish('{}')



