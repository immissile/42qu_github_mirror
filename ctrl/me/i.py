# -*- coding: utf-8 -*-
from _handler import LoginBase, XsrfGetBase
from ctrl._urlmap.me import urlmap
from zkit.pic import picopen
from zkit.jsdict import JsDict
from model.motto import motto as _motto
from model.user_info import UserInfo, user_info_new
from model.namecard import namecard_get, namecard_new
from model.ico import ico_new, ico_pos, ico_pos_new
from model.zsite_url import url_by_id, url_new, url_valid, RE_URL
from model.user_mail import mail_by_user_id
from model.txt import txt_get, txt_new
from model.mail_notice import CID_MAIL_NOTICE_ALL, mail_notice_all, mail_notice_set
from model.zsite import zsite_name_edit, user_can_reply, ZSITE_STATE_VERIFY, ZSITE_STATE_ACTIVE, ZSITE_STATE_WAIT_VERIFY, ZSITE_STATE_APPLY
from model.user_auth import user_password_new, user_password_verify
from model.user_mail import mail_by_user_id
from cgi import escape
from urlparse import parse_qs
from model.zsite_link import OAUTH2NAME_DICT, link_list_save, link_id_name_by_zsite_id, link_id_cid, link_by_id, OAUTH_LINK_DEFAULT
from urlparse import urlparse
from model.oauth2 import oauth_access_token_by_user_id, oauth_token_rm_if_can, OauthClient
from config import SITE_URL, SITE_DOMAIN
from model.oauth import OAUTH_DOUBAN, OAUTH_SINA, OAUTH_TWITTER, OAUTH_QQ, oauth_by_zsite_id, oauth_rm_by_oauth_id, OAUTH_SYNC_TXT 
from model.zsite import Zsite
from model.cid import CID_PO
from collections import defaultdict
from model.sync import sync_state_set, sync_all, sync_follow_new

OAUTH2URL = {
    OAUTH_DOUBAN:'http://www.douban.com/people/%s/',
    OAUTH_SINA:'http://weibo.com/%s',
    OAUTH_TWITTER:'http://twitter.com/%s',
    OAUTH_QQ:'http://t.qq.com/%s',
}

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


class LinkEdit(LoginBase):
    def _linkify(self, link, cid=0):
        link = link.strip().split(' ', 1)[0]
        if link:
            if cid in OAUTH2URL and RE_URL.match(link):
                link = OAUTH2URL[cid] % link
            elif not link.startswith('http://') and not link.startswith('https://'):
                link = 'http://%s'%link

        return link

    def get(self):
        zsite_id = self.zsite_id
        id_name = link_id_name_by_zsite_id(zsite_id)
        id_cid = dict(link_id_cid(zsite_id))

        link_list = []
        link_cid = []
        exist_cid = set()

        for id, name in id_name:
            link = link_by_id(id)
            if id in id_cid:
                cid = id_cid[id]
                link_cid.append((cid, name , link))
                exist_cid.add(cid)
            else:
                link_list.append((id, name, link))

        for cid in (set(OAUTH_LINK_DEFAULT) - exist_cid):
            link_cid.append((cid, OAUTH2NAME_DICT[cid], ''))

        return self.render(
            link_list=link_list,
            link_cid=link_cid
        )

    def save(self):
        zsite_id = self.zsite_id

        arguments = parse_qs(self.request.body, True)
        link_cid = []
        link_kv = []
        for cid, link in zip(arguments.get('cid'), arguments.get('link')):
            cid = int(cid)
            name = OAUTH2NAME_DICT[cid]
            link_cid.append((cid, name, self._linkify(link, cid)))


        for id, key, value in zip(
            arguments.get('id'),
            arguments.get('key'),
            arguments.get('value')
        ):
            id = int(id)
            link = self._linkify(value)

            link_kv.append((id, key.strip() or urlparse(link).netloc, link))

        link_list_save(zsite_id, link_cid, link_kv)



class CareerEdit(LoginBase):
    def get(self):
        from model.career import CID_JOB, CID_EDU, career_list
        current_user_id = self.current_user_id
        self.render(
            job_list=career_list(current_user_id, CID_JOB),
            edu_list=career_list(current_user_id, CID_EDU),
        )

    def save(self):
        from model.career import CID_TUPLE, career_list_set
        current_user_id = self.current_user_id
        #Tornado会忽略掉默认为空的参数
        arguments = parse_qs(self.request.body, True)

        for cid, prefix in CID_TUPLE:
            id = arguments.get('%s_id' % prefix, [])
            unit = arguments.get('%s_unit' % prefix, [])
            title = arguments.get('%s_title' % prefix, [])
            txt = arguments.get('%s_txt' % prefix, [])
            begin = arguments.get('%s_begin' % prefix, [])
            end = arguments.get('%s_end' % prefix, [])
            career_list_set(id, current_user_id, unit, title, txt, begin, end, cid)


class PicEdit(LoginBase):
    def get(self):
        current_user_id = self.current_user_id
        pos = ico_pos.get(current_user_id)
        self.render(pos=pos)

    def save(self):
        current_user_id = self.current_user_id
        files = self.request.files
        pos = self.get_argument('pos', '')
        if pos:
            ico_pos_new(current_user_id, pos)
        error_pic = _upload_pic(files, current_user_id)
        return error_pic



class UserInfoEdit(LoginBase):
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
            sex=o.sex
        )

    def save(self):
        current_user_id = self.current_user_id

        name = self.get_argument('name', None)
        if name:
            zsite_name_edit(current_user_id, name)

        motto = self.get_argument('motto', None)
        if motto:
            _motto.set(current_user_id, motto)

        txt = self.get_argument('txt', '')
        if txt:
            txt_new(current_user_id, txt)

        birthday = self.get_argument('birthday', '0')
        birthday = int(birthday)
        marry = self.get_argument('marry', '')
        pid_home = self.get_argument('pid_home', '1')
        pid_now = self.get_argument('pid_now', '1')
        try:
            pid_now = int(pid_now)
        except ValueError:
            pid_now = 0
        try:
            pid_home = int(pid_home)
        except ValueError:
            pid_home = 0

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



@urlmap('/i/pic')
class Pic(PicEdit):
    def post(self):
        error_pic = self.save()
        if error_pic:
            self.render(error_pic=error_pic)
        else:
            self.get()

@urlmap('/i/url')
class Url(LoginBase):
    def prepare(self):
        super(Url, self).prepare()
        if not self._finished:
            user = self.current_user
            user_id = self.current_user_id
            link = self.current_user.link
            if user.state <= ZSITE_STATE_APPLY:
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
                self.redirect(SITE_URL)
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
        if not self._finished:
            current_user = self.current_user
            current_user_id = self.current_user_id
            state = current_user.state
            if state >= ZSITE_STATE_VERIFY:
                return self.redirect('/')
            elif state <= ZSITE_STATE_APPLY:
                return self.redirect('/auth/verify/sended/%s' % current_user_id)

    def post(self):
        current_user = self.current_user
        current_user.state = ZSITE_STATE_WAIT_VERIFY
        current_user.save()
        return self.get()

    def get(self):
        self.render()


@urlmap('/i/career')
class Career(CareerEdit):
    def post(self):
        self.save()
        self.get()


@urlmap('/i')
class Index(UserInfoEdit):
    def post(self):
        files = self.request.files
        current_user_id = self.current_user_id
        self.save()
        self.get()


@urlmap('/i/link')
class Link(LinkEdit):
    def post(self):
        self.save()
        self.get()


class NameCardEdit(object):
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
        )

    def save(self):
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
            return c


@urlmap('/i/namecard')
class Namecard(NameCardEdit, LoginBase):
    def post(self):
        self.save()
        self.get()


@urlmap('/i/mail/notice')
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
        self.get()



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

@urlmap('/i/invoke')
class Invoke(LoginBase):
    def get(self):
        user_id = self.current_user_id
        li = oauth_access_token_by_user_id(user_id)
        OauthClient.mc_bind(li, 'client', 'client_id')
        Zsite.mc_bind(li, 'user', 'user_id')
        self.render(li=li)

@urlmap('/i/invoke/rm/(\d+)')
class InvokeRm(XsrfGetBase):
    def get(self, id):
        if id:
            user_id = self.current_user_id
            oauth_token_rm_if_can(id, user_id)
            self.redirect('/i/invoke')

@urlmap('/i/bind/(\d+)')
class BindItem(LoginBase):
    def get(self, id):
        return self.render(id=id)


@urlmap('/i/bind')
class Bind(LoginBase):
    def get(self):
        user_id = self.current_user_id

        app_dict = defaultdict(list)

        for app_id , oauth_id in oauth_by_zsite_id(user_id):
            app_dict[app_id].append(oauth_id)        

        self.render(
            sync_list=sync_all(user_id), app_dict=app_dict
        )

#    def post(self):
#        user_id = self.current_user_id
#        for cid in CID_PO:
#            state = self.get_argument('cid%s' % cid, None)
#            sync_state_set(user_id, cid, state)
#        self.get()


@urlmap('/i/binded/(\d+)')
class Binded(LoginBase):
    def get(self, cid):
        self.render(cid=cid, txt=OAUTH_SYNC_TXT)

    def post(self, cid):
        fstate = self.get_argument('fstate', None)
        tstate = self.get_argument('tstate', None)
        txt = self.get_argument('weibo', None)

        user_id = self.current_user_id

        flag = 0
        if fstate:
            flag += 0b1
        if tstate:
            flag += 0b10

        sync_follow_new(user_id, flag, cid, txt)
        
        url = 'http://rpc.%s/oauth/%s'%(SITE_DOMAIN, cid)
        
        self.redirect(url)


@urlmap('/i/bind/oauth_rm/(\d+)')
class BindOauthRm(XsrfGetBase):
    def get(self, id):
        if id:
            oauth_rm_by_oauth_id(id)
        self.redirect('/i/bind')

