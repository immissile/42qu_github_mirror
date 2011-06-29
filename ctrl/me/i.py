# -*- coding: utf-8 -*-
from _handler import LoginBase
from ctrl._urlmap.me import urlmap
from zkit.pic import picopen
from zkit.jsdict import JsDict
from model.motto import motto as _motto
from model.namecard import namecard_get, namecard_new
from model.ico import ico_new, ico_pos, ico_pos_new
from model.zsite_link import url_by_id, url_new, url_valid
from model.user_mail import mail_by_user_id
from model.txt import txt_get, txt_new
from model.mail_notice import CID_MAIL_NOTICE_ALL, mail_notice_all, mail_notice_set
from model.zsite import user_can_reply, ZSITE_STATE_VERIFY, ZSITE_STATE_ACTIVE, ZSITE_STATE_WAIT_VERIFY, ZSITE_STATE_APPLY
from model.user_auth import user_password_new, user_password_verify, user_new_by_mail
from model.user_mail import mail_by_user_id
from cgi import escape


def _upload_pic(files, current_user_id):
    error_pic = None
    if 'pic' in files:
        pic = files['pic'][0]['body']
        pic = picopen(pic)
        if pic:
            ico_new(current_user_id, pic)
            error_pic = False
        else:
            error_pic = '图片格式有误'
    return error_pic


@urlmap('/i/pic')
class Pic(LoginBase):
    def get(self):
        current_user_id = self.current_user_id
        pos = ico_pos.get(current_user_id)
        self.render(pos=pos)

    def post(self):
        current_user_id = self.current_user_id
        files = self.request.files
        pos = self.get_argument('pos', '')
        if pos:
            ico_pos_new(current_user_id, pos)
        error_pic = _upload_pic(files, current_user_id)
        self.render(error_pic=error_pic, pos=pos)


@urlmap('/i/url')
class Url(LoginBase):
    def prepare(self):
        super(Url, self).prepare()
        if not self._finished:
            user = self.current_user
            user_id = self.current_user_id
            link = self.current_user.link
            if not user.state <= ZSITE_STATE_APPLY:
                self.redirect(link+'/i/verify')
            elif url_by_id(user_id):
                self.redirect(link)

    def get(self):
        self.render(url='')

    def post(self):

        user_id = self.current_user_id
        url = self.get_argument('url', None)
        if url:
            if url_by_id(user_id):
                error_url = '个性域名设置后不能修改'
            else:
                error_url = url_valid(url)
            if error_url is None:
                url_new(user_id, url)
        else:
            error_url = '个性域名不能为空'
        self.render(
            error_url=error_url,
            url=url
        )


@urlmap('/i/verify')
class Verify(LoginBase):
    def prepare(self):
        super(Verify, self).prepare()
        current_user = self.current_user
        state = current_user.state
        if state >= ZSITE_STATE_VERIFY:
            return self.redirect('/')
        elif state <= ZSITE_STATE_APPLY:
            return self.redirect('/auth/verify/sended')

    def post(self):
        current_user = self.current_user
        current_user.state = ZSITE_STATE_WAIT_VERIFY
        current_user.save()
        return self.get()

    def get(self):
        self.render()


@urlmap('/i')
class Index(LoginBase):
    def get(self):
        current_user_id = self.current_user_id
        current_user = self.current_user
        motto = _motto.get(current_user_id),
        txt = txt_get(current_user_id)
        c = namecard_get(current_user_id) or JsDict()
        self.render(
            name=current_user.name,
            motto=motto,
            txt=txt,
            birthday=str(c.birthday).zfill(8),
            pid_now=c.pid_now or 0,
            pid_home=c.pid_home or 0,
        )


    def post(self):
        files = self.request.files
        current_user_id = self.current_user_id
        current_user = self.current_user

        name = self.get_argument('name', None)
        if name:
            current_user.name = name
            current_user.save()

        motto = self.get_argument('motto', None)
        if motto:
            _motto.set(current_user_id, motto)

        error_pic = _upload_pic(files, current_user_id)
        if error_pic is False:
            return self.redirect('/i/pic')

        txt = self.get_argument('txt', '')
        if txt:
            txt_new(current_user_id, txt)

        self.render(
            error_pic=error_pic,
            txt=txt,
            name=current_user.name,
        )


@urlmap('/i/namecard')
class Namecard(LoginBase):
    def get(self):
        current_user = self.current_user
        current_user_id = self.current_user_id
        c = namecard_get(current_user_id) or JsDict()
        self.render(
            name=c.name or current_user.name,
            phone=c.phone,
            mail=c.mail or mail_by_user_id(current_user_id),
            pid_now=c.pid_now or 0,
            address=c.address,
            sex=c.sex,
        )

    def post(self):
        current_user = self.current_user
        current_user_id = self.current_user_id
        pid_now = self.get_argument('pid_now', '1')
        name = self.get_argument('name', '')
        sex = self.get_argument('sex', '')
        phone = self.get_argument('phone', '')
        mail = self.get_argument('mail', '')
        address = self.get_argument('address', '')

        pid_now = int(pid_now)

        c = namecard_get(current_user_id) or JsDict()
        sex = c.sex
        if not sex:
            sex = int(sex)
            if sex not in (1, 2):
                sex = 0

        if pid_now or name or phone or mail or address or sex:
            c = namecard_new(
                current_user_id, sex, marry, birthday,
                pid_home, pid_now, name, phone, mail, address
            )

        self.render(
            pid_now=pid_now,
            name=name or current_user.name,
            phone=phone,
            mail=mail,
            address=address,
            birthday=birthday,
            sex=sex,
        )


@urlmap('/i/mail_notice')
class MailNotice(LoginBase):
    def get(self):
        user_id = self.current_user_id
        self.render(
            mail_notice_all=mail_notice_all(user_id)
        )

    def post(self):
        user_id = self.current_user_id
        for cid in CID_MAIL_NOTICE_ALL:
            state = self.get_argument('mn%s' % cid, None)
            mail_notice_set(user_id, cid, state)
        self.redirect('/i/mail_notice')



@urlmap('/i/password')
class Password(LoginBase):
    def get(self):
        self.render()

    def post(self):
        user_id = self.current_user_id
        password0 = self.get_argument('password0', None)
        password = self.get_argument('password', None)
        password2 = self.get_argument('password2', None)
        success = None
        error_password = None
        if all((password0, password, password2)):
            if password == password2:
                if user_password_verify(user_id, password0):
                    user_password_new(user_id, password)
                    success = True
                else:
                    error_password = '密码有误。忘记密码了？<a href="/auth/password/reset/%s">点此找回</a>' % escape(mail_by_user_id(user_id))
            else:
                error_password = '两次输入密码不一致'
        else:
            error_password = '请输入密码'
        self.render(
            success=success,
            error_password=error_password
        )
