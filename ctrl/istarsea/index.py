# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.istarsea import urlmap
from zkit.txt import EMAIL_VALID, mail2link
from zkit.errtip import Errtip
from model.user_mail import mail_by_user_id, user_id_by_mail
from model.user_auth import user_password_new, user_password_verify, user_new_by_mail
from model.user_new import user_new
from model.user_session import user_session, user_session_rm
from model.namecard import namecard_new

@urlmap('/')
class Index(Base):
    def get(self):
        return self.render(
            errtip=Errtip()
        )


    def post(self):
        name = self.get_argument('name', '')
        mail = self.get_argument('mail', '')
        errtip = Errtip()
        if mail:
            mail = mail.lower()
        if not mail:
            errtip.mail = '请输入邮箱'
        elif not EMAIL_VALID.match(mail):
            errtip.mail = '邮箱格式有误'

        if not name:
            errtip.name = '请输入姓名'


        if not errtip:
            user_id = user_id_by_mail(mail)
            if not user_id:
                user_id = user_new(mail, name=name)
                session = user_session(user_id)
                self.set_cookie('S', session)
                self.set_cookie('E', mail)

                phone = self.get_argument('phone', '')
                namecard_new(user_id,phone=phone)

                return self.redirect('/reged/%s'%user_id)

        self.render(
            mail=mail,
            name=name,
            errtip=errtip
        )

@urlmap('/reged/(\d+)')
class Reged(Base):
    def get(self, user_id):
        return self.render()
