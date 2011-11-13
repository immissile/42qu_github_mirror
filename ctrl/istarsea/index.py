# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.istarsea import urlmap
from zkit.txt import EMAIL_VALID, mail2link
from zkit.errtip import Errtip
from model.user_mail import mail_by_user_id, user_id_by_mail
from model.user_auth import user_password_new, user_password_verify, user_new_by_mail

@urlmap('/')
class Index(Base):
    def get(self):
#        current_user = self.current_user
#        if current_user:
#            self.redirect(
#                '%s/live'%current_user.link
#            )
#        else:
#            self.redirect('/login')

        return self.render(
            errtip=Errtip()
        )


    def post(self):
        name = self.get_argument('name', '')
        mail = self.get_argument('mail', '')
        if mail:
            mail = mail.lower()
        if not mail:
            errtip.mail = '请输入邮箱'
        elif not EMAIL_VALID.match(mail):
            errtip.mail = '邮箱格式有误'

        if not name:
            errtip.password = '请输入姓名'

        if not errtip:
            user_id = user_id_by_mail(mail)
            if not user_id:
                user = user_new_by_mail(mail, 'istarsea')
                user_id = user.id
                user_info_new(user_id, sex=sex)
                search_new(user_id)        
    
        self.render(
            mail=mail,
            name=name,
            errtip=errtip
        )
