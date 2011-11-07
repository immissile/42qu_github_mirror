# -*- coding: utf-8 -*-
from ctrl.main._handler import Base, LoginBase, XsrfGetBase
from cgi import escape
from ctrl._urlmap.auth import urlmap
from model.cid import CID_VERIFY_MAIL, CID_VERIFY_PASSWORD, CID_USER, CID_VERIFY_COM
from model.user_mail import mail_by_user_id, user_id_by_mail
from model.user_session import user_session, user_session_rm
from model.verify import verify_mail_new, verifyed
from model.zsite import Zsite, ZSITE_STATE_APPLY, ZSITE_STATE_ACTIVE
from model.user_auth import user_password_new, user_password_verify
from zkit.txt import EMAIL_VALID, mail2link
from model.zsite_site import site_can_admin
from model.job_mail import JobMail, STATE_VERIFIED, STATE_VERIFY 

@urlmap('/auth/verify/send/(\d+)')
class Send(Base):
    cid = CID_VERIFY_MAIL
    def get(self, id):
        user_id = int(id)
        user = Zsite.mc_get(id)
        if user.state == ZSITE_STATE_APPLY and user.cid == CID_USER:
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


@urlmap('/auth/verify/mail/(\d+)/(.+)')
class VerifyMail(VerifyBase):
    cid = CID_VERIFY_MAIL
    def get(self, id, ck):
        user_id = self.handler_verify(id, ck)
        if user_id:
            user = Zsite.mc_get(user_id)
            if user.state == ZSITE_STATE_APPLY:
                user.state = ZSITE_STATE_ACTIVE
                user.save()
            self.__dict__['_current_user'] = user
            self.render()

@urlmap('/job/auth/verify/mail/(\d+)/(.+)')
class JobVerifyMail(LoginBase):
    def get(self, id, ck):
        user_id, cid = verifyed(id, ck, delete=False)
        if user_id and CID_VERIFY_COM == cid and site_can_admin(user_id,self.current_user_id):
            jm = JobMail.get(zsite_id=user_id)
            if jm.state == STATE_VERIFY:
                jm.state = STATE_VERIFIED
                jm.save()
            self.render(jm=jm)
        else:
            self.redirect('/')

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
