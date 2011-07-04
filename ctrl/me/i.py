# -*- coding: utf-8 -*-
from _handler import LoginBase
from ctrl._urlmap.me import urlmap
from zkit.pic import picopen
from zkit.jsdict import JsDict
from model.motto import motto as _motto
from model.user_info import UserInfo, user_info_new
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
from urlparse import parse_qs


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

@urlmap('/i/career')
class Career(LoginBase):
    def get(self):
        return self.render()

    def post(self):
        #Tornado会忽略掉默认为空的参数
        arguments = parse_qs(self.request.body, True)

        def _(prefix):
            id = arguments.get('%s_id'%prefix, [])
            title = arguments.get('%s_title'%prefix, [])
            unit = arguments.get('%s_unit'%prefix, [])
            txt = arguments.get('%s_txt'%prefix, [])
            begin = arguments.get('%s_begin'%prefix, [])
            end = arguments.get('%s_end'%prefix, [])
            print id
            print title
            print unit
            print begin
            print end

        _('edu')
        _('job')

        return self.render()

class UserInfoEdit(object):
    def get(self):
        current_user_id = self.current_user_id
        current_user = self.current_user
        motto = _motto.get(current_user_id)
        txt = txt_get(current_user_id)
        o = UserInfo.mc_get(current_user_id) or JsDict()
        c = namecard_get(current_user_id) or JsDict()
        self.render(
            name=current_user.name,
            motto=motto,
            txt=txt,
            birthday='%08d' % (o.birthday or 0),
            marry=o.marry,
            pid_home=o.pid_home or 0,
            pid_now=c.pid_now or 0,
            sex = o.sex
        )

    def save(self):
        current_user_id = self.current_user_id
        current_user = self.current_user

        name = self.get_argument('name', None)
        if name:
            current_user.name = name
            current_user.save()

        motto = self.get_argument('motto', None)
        if motto:
            _motto.set(current_user_id, motto)

        txt = self.get_argument('txt', '')
        if txt:
            txt_new(current_user_id, txt)

        birthday = self.get_argument('birthday', '')
        marry = self.get_argument('marry', '')
        pid_home = self.get_argument('pid_home', '1')
        pid_now = self.get_argument('pid_now', '1')

        marry = int(marry)
        if marry not in (1, 2, 3):
            marry = 0

        o = user_info_new(current_user_id, birthday, marry, pid_home)
        if pid_now:
            c = namecard_get(current_user_id)
            if c:
                c.pid_now = pid_now
                c.save()
            else:
                c = namecard_new(current_user_id, pid_now=pid_now)
        

        if not o.sex:
            sex = self.get_argument('sex', 0)
            if sex and not o.sex:
                sex = int(sex)
                if sex not in (1, 2):
                    sex = 0
                if sex:
                    if o:
                        o.sex = sex
                        o.save()
                    else:
                        user_info_new(current_user_id, sex=sex)


@urlmap('/i')
class Index(UserInfoEdit, LoginBase):
    def post(self):
        files = self.request.files
        current_user_id = self.current_user_id

        error_pic = _upload_pic(files, current_user_id)
        if error_pic is False:
            return self.redirect('/i/pic')

        self.save()

        self.redirect('/i')

@urlmap('/i/link')
class Link(LoginBase):
    def get(self):
        link_list = []
        link_cid = {}
        return self.render(
            link_list = link_list,
            link_cid = link_cid
        ) 

    def post(self):
        return self.get()

@urlmap('/i/namecard')
class Namecard(LoginBase):
    def get(self):
        current_user = self.current_user
        current_user_id = self.current_user_id
        c = namecard_get(current_user_id) or JsDict()
        o = UserInfo.mc_get(current_user_id) or JsDict()
        self.render(
            name=c.name or current_user.name,
            phone=c.phone,
            mail=c.mail or mail_by_user_id(current_user_id),
            pid_now=c.pid_now or 0,
            address=c.address,
            sex=o.sex,
        )

    def post(self):
        current_user = self.current_user
        current_user_id = self.current_user_id
        pid_now = self.get_argument('pid_now', '1')
        name = self.get_argument('name', '')
        phone = self.get_argument('phone', '')
        mail = self.get_argument('mail', '')
        address = self.get_argument('address', '')

        pid_now = int(pid_now)


        if pid_now or name or phone or mail or address:
            c = namecard_new(
                current_user_id, pid_now, name, phone, mail, address
            )

        self.redirect('/i/namecard')


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
