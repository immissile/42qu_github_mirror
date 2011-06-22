# -*- coding: utf-8 -*-
from _handler import LoginBase
from ctrl._urlmap.me import urlmap
from zkit.pic import picopen
from zkit.jsdict import JsDict
from model.motto import motto
from model.namecard import namecard_get, namecard_new
from model.ico import ico_new, ico_pos, ico_pos_new
from model.zsite_link import url_by_id, url_new, url_valid
from model.user_mail import mail_by_user_id
from model.txt import txt_get, txt_new
from model.mail_notice import CID_MAIL_NOTICE_ALL, mail_notice_all, mail_notice_set
from model.zsite import user_can_reply, ZSITE_STATE_VERIFY, ZSITE_STATE_ACTIVE, ZSITE_STATE_WAIT_VERIFY, ZSITE_STATE_APPLY

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


@urlmap('/i')
class Index(LoginBase):
    def get(self):
        current_user_id = self.current_user_id
        txt = txt_get(current_user_id)
        self.render(txt=txt)

    def post(self):
        files = self.request.files
        current_user_id = self.current_user_id
        current_user = self.current_user

        _name = self.get_argument('name', None)
        if _name:
            current_user.name = _name
            current_user.save()

        _motto = self.get_argument('motto', None)
        if _motto:
            motto.set(current_user_id, _motto)

        error_pic = _upload_pic(files, current_user_id)
        if error_pic is False:
            return self.redirect('/i/pic')

        txt = self.get_argument('txt', '')
        if txt:
            txt_new(current_user_id, txt)

        self.render(
            error_pic=error_pic,
            txt=txt
        )


@urlmap('/i/url')
class Url(LoginBase):
    def prepare(self):
        super(Url, self).prepare()
        user = self.current_user
        user_id = self.current_user_id
        link = self.current_user.link
        if not user_can_reply(user):
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
            return self.redirect("/auth/verify/sended")

    def post(self):
        current_user = self.current_user
        current_user.state = ZSITE_STATE_WAIT_VERIFY
        current_user.save()
        return self.get()

    def get(self):
        self.render()


@urlmap('/i/namecard')
class Namecard(LoginBase):
    def get(self):
        current_user = self.current_user
        current_user_id = self.current_user_id
        c = namecard_get(current_user_id) or JsDict()
        pid_now = c.pid_now
        pid_home = c.pid_home
        birthday = str(c.birthday).zfill(8)
        self.render(
            sex=c.sex,
            marry=c.marry,
            pid_now=pid_now or 0,
            pid_home=pid_home or 0,
            name=c.name or current_user.name,
            phone=c.phone,
            mail=c.mail or mail_by_user_id(current_user_id),
            address=c.address,
            birthday=birthday
        )

    def post(self):
        current_user = self.current_user
        current_user_id = self.current_user_id
        pid_now = self.get_argument('pid_now', '1')
        pid_home = self.get_argument('pid_home', '1')
        name = self.get_argument('name', '')
        sex = self.get_argument('sex', '')
        marry = self.get_argument('marry', '')
        phone = self.get_argument('phone', '')
        mail = self.get_argument('mail', '')
        address = self.get_argument('address', '')
        birthday = self.get_argument('birthday', '00000000')

        pid_now = int(pid_now)
        pid_home = int(pid_home)
        birthday = int(birthday)
        sex = int(sex)
        if sex not in (1, 2):
            sex = 0
        marry = int(marry)
        if marry not in (1, 2, 3):
            marry = 0

        if pid_now or pid_home or name or \
            phone or mail or address or birthday \
            or sex or marry:
            c = namecard_new(
                current_user_id, sex, marry, birthday,
                pid_home, pid_now, name, phone, mail, address
            )

        self.render(
            marry=marry,
            pid_now=pid_now,
            pid_home=pid_home,
            name=name or current_user.name,
            phone=phone,
            mail=mail,
            address=address,
            birthday=birthday,
            sex=sex
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
        self.redirect('/i/notice')


