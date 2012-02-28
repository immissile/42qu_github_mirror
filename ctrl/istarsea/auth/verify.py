# -*- coding: utf-8 -*-

from ctrl.istarsea._handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap_istarsea.istarsea import urlmap
from cgi import escape
from model.cid import CID_VERIFY_MAIL, CID_VERIFY_PASSWORD, CID_USER, CID_VERIFY_COM_HR, CID_VERIFY_LOGIN_MAIL
from model.user_mail import mail_by_user_id, user_id_by_mail, user_mail_active_by_user
from model.user_session import user_session, user_session_rm
from model.verify import verify_mail_new, verifyed
from model.zsite import Zsite, ZSITE_STATE_APPLY, ZSITE_STATE_ACTIVE, ZSITE_STATE_NO_PASSWORD
from model.user_auth import user_password_new, user_password_verify
from zkit.txt import EMAIL_VALID, mail2link
from model.zsite_member import zsite_member_can_admin
from model.job_mail import job_mail_verifyed
from model.job import _job_pid_default_by_com_id
from model.zsite_url import link as _link

@urlmap('/auth/verify/send/(\d+)')
class Send(Base):
    cid = CID_VERIFY_MAIL
    def get(self, id):
        user_id = int(id)
        user = Zsite.mc_get(id)
        if user and user.state in (ZSITE_STATE_NO_PASSWORD, ZSITE_STATE_APPLY) and user.cid == CID_USER:
            mail = mail_by_user_id(user_id)
            verify_mail_new(user_id, user.name, mail, self.cid)
            path = '/auth/verify/sended/%s'%user_id
        else:
            path = '/login'

        self.redirect(path)


@urlmap('/auth/verify/sended/(\d+)')
class Sended(Base):
    def get(self, id):
        user_id = int(id)
        user = Zsite.mc_get(id)
        if user.state > ZSITE_STATE_APPLY or user.cid != CID_USER:
            return self.redirect('/login')
        return self.render(user_id=user_id)


class VerifyBase(Base):
    cid = None
    def handler_verify(self, id, ck, delete=False):
        user_id, cid = verifyed(id, ck, delete)
        if user_id and self.cid == cid:
            session = user_session(user_id)
            self.set_cookie('S', session)
            return user_id
        else:
            self.redirect('/')

@urlmap('/auth/verify/login/mail/(\d+)/(.+)')
class VerifyLoginMail(LoginBase):
    def get(self, id, ck):
        user_id, cid = verifyed(id, ck, delete=False)
        if user_id and CID_VERIFY_LOGIN_MAIL == cid:
            user = self.current_user
            user_mail_active_by_user(user)
            self.redirect('%s/i/account/mail/success'%user.link)
        else:
            self.redirect('/')


@urlmap('/auth/verify/mail/(\d+)/(.+)')
class VerifyMail(VerifyBase):
    cid = CID_VERIFY_MAIL
    def get(self, id, ck):
        user_id = self.handler_verify(id, ck)
        if user_id:
            user = Zsite.mc_get(user_id)
            if user.state == ZSITE_STATE_APPLY or user.state == ZSITE_STATE_NO_PASSWORD:
                user.state = ZSITE_STATE_ACTIVE
                user_mail_active_by_user(user)
                user.save()
            self.__dict__['_current_user'] = user

            redirect = self.get_argument('next', '%s/i/guide'%user.link)

            if redirect:
                return self.redirect(redirect)


@urlmap('/job/auth/verify/mail/(\d+)/(.+)')
class JobVerifyMail(LoginBase):
    def get(self, id, ck):
        user_id, cid = verifyed(id, ck, delete=False)

        if user_id and CID_VERIFY_COM_HR == cid and zsite_member_can_admin(user_id, self.current_user_id):
            job_mail_verifyed(user_id)
            link = _link(user_id)

            if _job_pid_default_by_com_id(user_id):
                path = '%s/job/admin/mail'
            else:
                path = '%s/job/new'
            path = path%link
        else:
            path = '/'

        self.redirect(path)

@urlmap('/auth/password/reset/(.+)')
class PasswordReset(Base):
    cid = CID_VERIFY_PASSWORD
    def get(self, mail):
        if mail.isdigit():
            user_id = mail
            user = Zsite.mc_get(user_id)
            if user:
                mail = mail_by_user_id(user_id)
                link = mail2link(mail)
                if user:
                    return self.render(mail=mail, link=link)
        elif EMAIL_VALID.match(mail):
            user_id = user_id_by_mail(mail)
            if user_id:
                user = Zsite.mc_get(user_id)
                verify_mail_new(user_id, user.name, mail, self.cid)
                return self.redirect('/auth/password/reset/%s'%user_id)
        self.redirect('/login')


@urlmap('/auth/verify/password/(\d+)/(.+)')
class VerifyPassword(VerifyBase):
    cid = CID_VERIFY_PASSWORD
    def get(self, id, ck):
        user_id = self.handler_verify(id, ck)
        if user_id:
            self.render()

    def post(self, id, ck):
        current_user_id = self.current_user_id
        current_user = self.current_user
        if current_user_id:
            password = self.get_argument('password', None)
            if password:
                user_id = self.handler_verify(id, ck, True)
                if current_user_id == user_id:
                    if current_user.state == ZSITE_STATE_APPLY:
                        current_user.state = ZSITE_STATE_ACTIVE
                        current_user.save()
                    user_password_new(user_id, password)
                    return self.render(password=password)
                else:
                    return
            else:
                return self.get(id, ck)
        self.redirect('/')


