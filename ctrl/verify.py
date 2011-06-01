#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from zweb._urlmap import urlmap
from zkit.txt import EMAIL_VALID, mail2link
from model.cid import CID_VERIFY_MAIL, CID_VERIFY_PASSWORD
from model.user_auth import user_password_new
from model.user_mail import mail_by_user_id, user_id_by_mail
from model.verify import verify_new, verify
from model.zsite import Zsite, ZSITE_STATE_APPLY, ZSITE_STATE_ACTIVE
from model.user_session import user_session

@urlmap('/verify/mail')
class Mail(LoginBase):
    cid = CID_VERIFY_MAIL
    def get(self):
        current_user = self.current_user
        current_user_id = self.current_user_id
        if current_user.state == ZSITE_STATE_APPLY:
            mail = mail_by_user_id(current_user_id)
            verify_new(current_user_id, current_user.name, mail, self.cid)
            link = mail2link(mail)
            return self.render(
                mail=mail,
                link=link,
            )
        self.redirect('/')

class VerifyBase(Base):
    cid = None
    def handler_verify(self, id, ck, delete=False):
        user_id, cid = verify(id, ck, delete)
        if user_id and self.cid == cid:
            session = user_session(user_id)
            self.set_cookie('S', session)
            return user_id
        else:
            self.redirect('/')

@urlmap('/verify/mail/(\d+)/(.+)')
class VerifyMail(VerifyBase):
    cid = CID_VERIFY_MAIL
    def get(self, id, ck):
        user_id = self.handler_verify(id, ck)
        if user_id:
            user = Zsite.mc_get(user_id)
            if user.state == ZSITE_STATE_APPLY:
                user.state = ZSITE_STATE_ACTIVE
                user.save()
            self.render()

@urlmap('/password/(.+)')
class Password(Base):
    cid = CID_VERIFY_PASSWORD
    def get(self, mail):
        if EMAIL_VALID.match(mail):
            user_id = user_id_by_mail(mail)
            if user_id:
                user = Zsite.mc_get(user_id)
                verify_new(user_id, user.name, mail, self.cid)
                link = mail2link(mail)
                return self.render(
                    mail=mail,
                    link=link,
                )
        self.redirect('/')

@urlmap('/verify/password/(\d+)/(.+)')
class VerifyPassword(VerifyBase):
    cid = CID_VERIFY_PASSWORD
    def get(self, id, ck):
        user_id = self.handler_verify(id, ck)
        if user_id:
            self.render()

    def post(self, id, ck):
        current_user_id = self.current_user_id
        if current_user_id:
            password = self.get_argument('password', None)
            if password:
                user_id = self.handler_verify(id, ck, True)
                if current_user_id == user_id:
                    user_password_new(user_id, password)
                    return self.render(password=password)
            else:
                return self.get(id, ck)
        self.redirect('/')
