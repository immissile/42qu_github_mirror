#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import LoginBase
from _urlmap import urlmap
from config import SITE_URL, SITE_DOMAIN
from model.invite_email import CID_GOOGLE, CID_QQ, CID_MSN, invite_email_new, msn_friend_get, invite_user_id_by_cid
import tornado.web
import thread
from zweb.json import jsonp
from yajl import dumps
from mixin import GoogleMixin
import re
from json import dumps, loads
from random import random
from urllib import urlencode
import cookielib, urllib2
from urllib2 import Request
from uuid import uuid4 as uuname
import gdata.contacts
import gdata.contacts.service
import gdata.auth
from gdata.service import RequestError
SIG_METHOD = gdata.auth.OAuthSignatureMethod.HMAC_SHA1

@urlmap('/invite/%s'%CID_MSN)
class MsnAsync(LoginBase):
    @tornado.web.asynchronous
    def get(self):
        email = self.get_argument('email', None)
        passwd = self.get_argument('passwd', None)
        url = 'http://%s.%s'%(self.current_user_id, SITE_DOMAIN)
        if email and passwd:
            thread.start_new_thread(
            self._load_friend,
            (email, passwd)
            )
        else:
            return self.finish(jsonp(self, dumps({'error':'输入正确的邮箱和密码'})))

    def _load_friend(self, email, passwd):
        res = msn_friend_get(email, passwd)
        if res:
            invite_email_new(self.current_user_id, CID_MSN, res)
            return self.finish(jsonp(self, dumps({'error':False, 'next':invite_user_id_by_cid(self.current_user_id, CID_MSN)})))
        else:
            return self.finish(jsonp(self, dumps({'error':'邮箱或密码错误'})))


@urlmap('/invite/%s'%CID_GOOGLE)
class GoogleAsync(LoginBase, GoogleMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument('oauth_token', None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authorize_redirect(
                self.callback_url()
                )

    def _on_auth(self, userj):
        email = None
        if userj:
            email = userj.get('uid')

        if not email:
            self.redirect('/invite/%s'%CID_GOOGLE)
            return

        user = self.current_user
        access_token = userj['access_token']
        key = access_token['key']
        secret = access_token['secret']
        user_id = str(user.id)



        thread.start_new_thread(
            self.async_load_friend,
            ( user_id, email, key, secret )
        )


    def async_load_friend(self, user_id, email, key, secret):
        result = load_friend(key, secret)
        if isinstance(result, list) and result:
            result = [[x, y] for x, y, z in result]
            _result = {}
            for i, j in result:
                _result[j] = i

            invite_email_new(user_id, CID_GOOGLE, _result)

            if invite_user_id_by_cid(self.current_user_id, CID_GOOGLE):
                return self.redirect('http://%s.%s/invite/show/%s'%(self.current_user_id, SITE_DOMAIN, CID_GOOGLE))
            else:
                self.redirect('http://%s.%s/invite/email'%(self.current_user_id, SITE_DOMAIN))


#return self.finish(jsonp(self,dumps({"error":False,"next":invite_user_id_by_cid(self.current_user_id,CID_GOOGLE)})))



def load_friend(TOKEN, TOKEN_SECRET):
    from config import GOOGLE_CONSUMER_KEY, GOOGLE_CONSUMER_SECRET
    client = gdata.contacts.service.ContactsService(source=GOOGLE_CONSUMER_KEY)
    client.SetOAuthInputParameters(SIG_METHOD, GOOGLE_CONSUMER_KEY, consumer_secret=GOOGLE_CONSUMER_SECRET)

    token = gdata.auth.OAuthToken(key=TOKEN, secret=TOKEN_SECRET)
    token.scopes = 'http://www.google.com/m8/feeds/'
    token.oauth_input_params = client._oauth_input_params
    client.SetOAuthToken(token)


    query = gdata.contacts.service.ContactsQuery()
    query.max_results = 99999
    #query.start_index = 1
    feed = client.GetContactsFeed(query.ToUri())
    email_address = None
    result = [] #email,name,info
    for entry in feed.entry:
        name = entry.title.text
        for email in entry.email:
            email_address = email.address
        if email_address:
            email_address = email_address.strip().lower()
            if name is not None:
                name = name.strip()
            result.append((name, email_address, None))

#    result.sort(key=lambda x:email_rank(x[1]), reverse=True)
    return result


################################################

COOKIE_ATTR = (
'version',
 'name',
 'value',
 'port',
 'port_specified',
 'domain',
 'domain_specified',
 'domain_initial_dot',
 'path',
 'path_specified',
 'secure',
 'expires',
 'discard',
 'comment',
 'comment_url',
 'rest'
)
headers = {
'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5',
'Referer': 'http://mail.qq.com/cgi-bin/loginpage'
}

def dumps_cookiejar(jar):
    r = []
    for k in jar:
        v = {}
        for i in COOKIE_ATTR:
            s = getattr(k, i, None)
            if s is not None:
                v[i] = s
        r.append(v)
    return dumps(r)



def loads_cookiejar(s, enc='utf-8'):
    cookiejar = cookielib.CookieJar()
    for d in loads(s):
        ad = {}
        for i in COOKIE_ATTR:
            m = d.get(i)
            if type(m) is unicode:
                m = m.encode(enc)
            ad[i] = m
        cookiejar.set_cookie(cookielib.Cookie(**ad))
    return cookiejar


LOGIN_PAGE = 'http://mail.qq.com/cgi-bin/loginpage'
LOGIN_ACTION = re.compile(r'"(http://m\d+.mail.qq.com/cgi-bin/login[^"]*)')
PUBLIC_KEY = re.compile('PublicKey\s*=\s*"(\w+)";')
PUBLIC_TS = re.compile('PublicTs\s*=\s*"(\d+)";')
QQ_POST = re.compile("""action="(http://m\d+\.mail.qq.com/cgi-bin/[^"]+)""")
QQ_POST_HOST = re.compile("""(http://m\d+\.mail.qq.com)""")
QQ_LOGIN_ERR_TYPE = {
'1':'您填写的帐号或密码不正确，请再次尝试。',
'2':'您填写的验证码不正确。',
'3':'您登录次数过于频繁，为保障安全，请输入验证码。',
'4':'您的邮箱设置了“独立密码”',
}
ERR_TIP = re.compile(r'''"errtype=(\d+)"''')
SID = re.compile(r'''sid=([^"]*)''')
def parse_contact_html(html):
    result = {}
    s = html.replace('\n', '').split('<div class="M">')
    for i in s:
        if i.find('type="checkbox" name="AddrID"') > 0:
            email = RE_EMAIL.search(i)
            nick = RE_NICK.search(i)
            name = RE_NAME.search(i)
            name = name.groups()[0]
            nick = nick.groups()[0]
            email = email.groups()[0].lower()
            if nick and name:
                showname = '%s (%s)'%(nick, name)
            elif nick or name:
                showname = nick or name
            else:
                showname = email.split('@', 1)[0]
            result[email] = showname
    return result

def _async_login(callback, arguments):
    for k, v in arguments.items():
        if type(v) is list:
            arguments[k] = v and v[0]
    qq_cookie = arguments['qq_cookie']
    del arguments['qq_cookie']
    url = arguments['qq_action']
    del arguments['qq_action']
    arguments['s'] = ''
    arguments['f'] = 'html'
    arguments['redirecturl'] = ''
    arguments['from'] = ''
    arguments['delegate_url'] = ''
    cookiejar = loads_cookiejar(qq_cookie)
    cookie_handler = urllib2.HTTPCookieProcessor(cookiejar)
    opener = urllib2.build_opener()
    opener.add_handler(cookie_handler)
    urlopen = opener.open
    data = urlencode(arguments)
    request = Request(url, headers=headers)
    content = urlopen(request, data, timeout=30).read().decode('gb18030', 'ignore')
    err = ERR_TIP.search(content)
    if err:
        r = "{error:'%s'}"%str(QQ_LOGIN_ERR_TYPE.get(err.groups()[0]))
    else:
        sid = SID.search(content)
        if sid:
            sid = sid.groups()[0]
            r = True
        else:
            r = "{error:'未知错误'}"
            print content

    if r is True:
        r = {}
        host = QQ_POST_HOST.search(url).groups()[0]
        improt_qq_url = host+'/cgi-bin/addr_importqq?sid='+sid
        urlopen(improt_qq_url, timeout=30).read()
        contact_qq_url = host + '/cgi-bin/addr_listall?type=user&sid=%s&category=all'%sid
        html = urlopen(contact_qq_url, timeout=30).read()
        html = html.decode('gb18030', 'ignore')
        r = dumps( parse_contact_html( html ).items() )
    callback(r)

def _async_get_verify(callback):
    request = Request(LOGIN_PAGE, headers=headers)

    login_page = urllib2.urlopen(request, timeout=30).read()

    ts = PUBLIC_TS.search(login_page)
    if ts:
        ts = ts.groups()[0]

    qq_post = QQ_POST.search(login_page)
    if qq_post:
        qq_post = qq_post.groups()[0]

    key = PUBLIC_KEY.search(login_page)
    if key:
        key = key.groups()[0]

    if None in (key, ts, qq_post):
        callback(None)
        return

    verifyimage_prefix = '/cgi-bin/getverifyimage'
    verifyimage_prefix_begin = login_page.find(verifyimage_prefix)

    if verifyimage_prefix_begin == '-1':
        callback(None)
        return

    imgurl = QQ_POST_HOST.search(qq_post).groups()[0] + login_page[
        verifyimage_prefix_begin
            :
        login_page.find("'", verifyimage_prefix_begin)
    ]+str(random())

    cookiejar = cookielib.CookieJar()
    cookie_handler = urllib2.HTTPCookieProcessor(cookiejar)
    opener = urllib2.build_opener()
    opener.add_handler(cookie_handler)
    urlopen = opener.open
    request = Request(imgurl, headers=headers)
    imgcontent = urlopen(request, timeout=30).read()
    imgkey = uuname().hex
    mc.set(imgkey, imgcontent, 6000)
    result = {
        'img':imgkey,
        'jar':dumps_cookiejar(cookiejar),
        'ts':ts,
        'key':key,
        'action':qq_post
    }
    r = dumps(result)
    callback(r)
class Mc(object):
    def __init__(self):
        self._o = {}
    def set(self, key, value, expires=None):
        self._o[key] = value
    def get(self, key):
        return self._o.get(key)
    def delete(self, key):
        if key in self._o:
            del self._o[key]
mc = Mc()

@urlmap('/invite/qq/?')
class ImportQqHandler(LoginBase):
    @tornado.web.asynchronous
    def post(self):
        _async_login( self.async_callback(self._on_done), self.request.arguments)


    def _on_done(self, r):
        if r is None:
            r = '{"error":"result is None"}'
        self.finish(jsonp(self, dumps(r)))


@urlmap('/invite/qq_verify')
class ImportQqVerifyHandler(LoginBase):
    @tornado.web.asynchronous
    def get(self):
        print 'do something'
        _async_get_verify( self.async_callback(self._on_get) )

    post = get
    def _on_get(self, r):
        if r is None:
            r = '{"error":"result is None"}'
        self.finish(jsonp(self, dumps(r)))


@urlmap('/invite/qq_img')
class ImportQqImgHandler(LoginBase):
    def get(self, key):
        self.set_header('Content-Type', 'image/png; charset=gbk')
        self.finish(jsonp(self, dumps(str(mc.get(key)))))
    post = get





if __name__ == '__main__':
    print tornado.auth.__file__









#
#
#
#
#
#@urlmap('/')
#class GoogleHandler(LoginBase,GoogleMixin):
#    @tornado.web.asynchronous
#    def get(self):
#        if self.get_argument("openid.mode", None):
#            self.get_authenticated_user(self.async_callback(self._on_auth))
#            return
#
#        self.authorize_redirect("http://www.google.com/m8/feeds/", ax_attrs=["name", "email"])
#
#    def _on_auth(self, userj):
#        email = None
#
#        if userj:
#            email = userj.get("email")
#
#        if not email:
#            self.redirect("/me/load_friend")
#            return
#
#        user = self.get_user()
#        if user is None:
#            self.redirect("/auth/login")
#            return
#
#        access_token = userj['access_token']
#        key = access_token['key']
#        secret = access_token['secret']
#        user_id = str(user.id)
#
#        if user.email == email:#TODO 支持多个email
#            oauth_save_google(user_id, key, secret)
#
#        thread.start_new_thread(
#            async_load_friend,
#            ( user_id, key, secret, self.async_callback(self._load_friend))
#        )
#
#    def _load_friend(self, save_id):
#        self.redirect("/me/load_friend/loaded/%s"%save_id)
#        self.finish()
