# -*- coding: utf-8 -*-
from ctrl.main._handler import Base, LoginBase, XsrfGetBase
from cgi import escape
from ctrl._urlmap.auth import urlmap
from model.cid import CID_VERIFY_MAIL, CID_VERIFY_PASSWORD
from model.namecard import namecard_get, namecard_new
from model.user_auth import user_password_new, user_password_verify, user_new_by_mail
from model.user_mail import mail_by_user_id, user_id_by_mail
from model.user_session import user_session, user_session_rm
from model.verify import verify_mail_new, verifyed
from model.zsite import Zsite, ZSITE_STATE_APPLY, ZSITE_STATE_ACTIVE
from zkit.txt import EMAIL_VALID, mail2link
from zkit.errtip import Errtip
from model.user_new import user_new

LOGIN_REDIRECT = '%s/live'

@urlmap('/logout')
class Logout(XsrfGetBase):
    def get(self):
        self.clear_cookie('S')
        current_user = self.current_user
        if current_user:
            user_session_rm(current_user.id)
        self.redirect('/')

class NoLoginBase(Base):
    def prepare(self):
        super(NoLoginBase, self).prepare()
        current_user = self.current_user
        if current_user:
            self.redirect(LOGIN_REDIRECT%current_user.link)

    def _login(self, user_id, mail, redirect=None):
        session = user_session(user_id)
        self.set_cookie('S', session)
        self.set_cookie('E', mail)
        if not redirect:
            current_user = Zsite.mc_get(user_id)
            redirect = LOGIN_REDIRECT%current_user.link
        self.redirect(redirect)

SHOW_LIST = (10074584, 10001433, 10054091, 10024555, 10014854, 10061647, 10002480, 10003683, 10007880, 10032093, 10014869, 10000144, 10024889, 10002312, 10003144, 10005102, 10022529, 10009692, 10000895, 10023650, 10006677, 10001875, 10017914, 10004712, 10016542, 10005981, 10055189, 10010156, 10073373, 10015306, 10009186, 10001929, 10010448, 10051930, 10018133, 10066598, 10028737, 10002687, 10029177, 10008285, 10068652, 10014849, 10011065, 10008692, 10000833, 10029871, 10025636, 10000645, 10000053, 10009225, 10002767, 10009040, 10060523, 10024538, 10001565, 10031402, 10000003, 10014236, 10000619, 10021794, 10014495, 10001397, 10003179, 10026510, 10071965, 10011811, 10009308, 10018282, 10055940, 10002178, 10055228, 10016550, 10019718, 10009854, 10016602, 10007895, 10002709)

@urlmap('/auth/reg/?(.*)')
class Reg(NoLoginBase):
    def get(self, mail=''):
        id_list = SHOW_LIST
        zsite_list = filter(bool, Zsite.mc_get_list(id_list))
        self.render(
            mail=mail,
            sex=0,
            password='',
            errtip=Errtip(),
            zsite_list=zsite_list,
        )

    def post(self, mail=None):
        mail = self.get_argument('mail', '')
        password = self.get_argument('password', '')
        sex = self.get_argument('sex', '0')
        errtip = Errtip()
        if sex:
            sex = int(sex)
            if sex not in (1, 2):
                sex = 0

        if mail:
            mail = mail.lower()
        if not mail:
            errtip.mail = '请输入邮箱'
        elif not EMAIL_VALID.match(mail):
            errtip.mail = '邮箱格式有误'

        if not password:
            errtip.password = '请输入密码'

        if not errtip:
            user_id = user_id_by_mail(mail)
            if user_id:
                if user_password_verify(user_id, password):
                    return self._login(user_id, mail)
                else:
                    errtip.password = '邮箱已注册。忘记密码了？<a href="/auth/password/reset/%s">点此找回</a>' % escape(mail)

        if not sex:
            errtip.sex = '请选择性别'

        if not errtip:
            user_id = user_new(mail,password,sex=sex)
            return self.redirect('/auth/verify/send/%s'%user_id)

        self.render(
            sex=sex, password=password, mail=mail,
            errtip=errtip
        )


@urlmap('/login')
class Login(NoLoginBase):
    def get(self):
        if self.get_cookie('E'):
            url = '/auth/login'
        else:
            url = '/auth/reg'
        self.redirect(url)


@urlmap('/auth/login')
class AuthLogin(NoLoginBase):

    def get(self):
        self.render(
            errtip=Errtip()
        )


    def post(self):
        mail = self.get_argument('mail', None)
        password = self.get_argument('password', None)
        errtip = Errtip()

        if mail:
            mail = mail.lower()
        if not mail:
            errtip.mail = '请输入邮箱'
        elif not EMAIL_VALID.match(mail):
            errtip.mail = '邮箱格式有误'

        if not password:
            errtip.password = '请输入密码'

        if not errtip:
            user_id = user_id_by_mail(mail)
            if user_id:
                if user_password_verify(user_id, password):
                    return self._login(user_id, mail, self.get_argument('next', None))
                else:
                    errtip.password = '密码有误。忘记密码了？<a href="/auth/password/reset/%s">点此找回</a>' % escape(mail)
            else:
                errtip.mail = """此账号不存在 , <a href="/auth/reg/%s">点此注册</a>"""%escape(mail)

        self.render(
            mail=mail,
            password=password,
            errtip=errtip
        )
