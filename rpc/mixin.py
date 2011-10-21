#!/usr/bin/env python
#coding:utf-8
import tornado.auth
from tornado import escape
from urllib import quote
import urllib
from tornado import httpclient
import logging
import json
import urlparse
from config import DOUBAN_CONSUMER_KEY, DOUBAN_CONSUMER_SECRET, WWW163_CONSUMER_KEY, WWW163_CONSUMER_SECRET, QQ_CONSUMER_SECRET, QQ_CONSUMER_KEY, SINA_CONSUMER_SECRET, SINA_CONSUMER_KEY, SOHU_CONSUMER_SECRET, SOHU_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_CONSUMER_KEY, RENREN_CONSUMER_KEY, RENREN_CONSUMER_SECRET

def callback_url(self):
    redirect_url = self.get_argument('path', None)
    path = self.request.path
    if redirect_url:
        if redirect_url[0] != '/':
            redirect_url = '/'+redirect_url
        path = path + '?path=%s'%quote(redirect_url)
    print path,'!!!!!!'
    return path


def xxx_request(self, path, callback, access_token=None, post_args=None, **args):
    url = self._API_URL%path
    if access_token:
        all_args = {}
        all_args.update(args)
        all_args.update(post_args or {})
        consumer_token = self._oauth_consumer_token()
        method = 'POST' if post_args is not None else 'GET'
        oauth = self._oauth_request_parameters(
            url, access_token, all_args, method=method)
        args.update(oauth)
    if args: url += '?' + urllib.urlencode(args)
    callback = self.async_callback(self._on_request, callback)
    http = httpclient.AsyncHTTPClient()
    if post_args is not None:
        print url, post_args
        http.fetch(url, method='POST', body=urllib.urlencode(post_args),
                   callback=callback)
    else:
        http.fetch(url, callback=callback)

def _parse_user_response(self, callback, txt):
    if txt:
        user = json.loads(txt)
    else:
        user = None
    callback(user)

def _on_request(self, callback, response):
    if response.error:
        logging.warning('Error response %s fetching %s', response.error,
                        response.request.url)
        callback(None)
        return
    callback(response.body)


class DoubanMixin(tornado.auth.OAuthMixin):
    _OAUTH_REQUEST_TOKEN_URL = 'http://www.douban.com/service/auth/request_token'
    _OAUTH_ACCESS_TOKEN_URL = 'http://www.douban.com/service/auth/access_token'
    _OAUTH_AUTHORIZE_URL = 'http://www.douban.com/service/auth/authorize'
    _OAUTH_VERSION = '1.0'
    _OAUTH_NO_CALLBACKS = False
    _on_request = _on_request
    callback_url = callback_url
    def douban_request(self, path, callback, access_token=None,
                           post_args=None, **args):
        # Add the OAuth resource request signature if we have credentials
        url = 'http://api.douban.com%s'%path
        if access_token:
            all_args = {}
            all_args.update(args)
            all_args.update(post_args or {})
            consumer_token = self._oauth_consumer_token()
            method = 'POST' if post_args is not None else 'GET'
            oauth = self._oauth_request_parameters(
                url, access_token, all_args, method=method)
            args.update(oauth)
        if args: url += '?' + urllib.urlencode(args)
        callback = self.async_callback(self._on_request, callback)
        http = httpclient.AsyncHTTPClient()
        if post_args is not None:
            http.fetch(url, method='POST', body=urllib.urlencode(post_args),
                       callback=callback)
        else:
            http.fetch(url, callback=callback)


    def _oauth_consumer_token(self):
        return dict(
            key=DOUBAN_CONSUMER_KEY,
            secret=DOUBAN_CONSUMER_SECRET)

    def _oauth_get_user(self, access_token, callback):
        callback = self.async_callback(self._parse_user_response, callback)
        douban_user_id = access_token['douban_user_id']
        self.douban_request(
            '/people/%s'%douban_user_id,
            access_token=access_token, callback=callback
        )


    def _parse_user_response(self, callback, xml):
        if xml:
            from BeautifulSoup import BeautifulStoneSoup
            soup = BeautifulStoneSoup(xml)
            user = dict(
                name=soup.title.string,
                uid=soup.find('db:uid').string
            )
        else:
            user = None
        callback(user)


class GoogleMixin(tornado.auth.GoogleMixin):
    """
    http://openid.net.cn/specs/openid-authentication-2_0-zh_CN.html
    OpenID认证2.0——最终版

    http://code.google.com/apis/accounts/docs/OpenID.html
    Federated Login for Google Account Users

    https://www.google.com/accounts/ManageDomains
    Google openid api key

    http://code.google.com/intl/zh-CN/apis/contacts/

    http://code.google.com/intl/zh-CN/apis/contacts/docs/1.0/developers_guide_python.html
    """
    _OAUTH_VERSION = '1.0'
    callback_url = callback_url

class RenrenMixin(tornado.auth.OAuth2Mixin):
    _OAUTH_AUTHORIZE_URL = 'https://graph.renren.com/oauth/authorize'
    _OAUTH_ACCESS_TOKEN_URL = 'https://graph.renren.com/oauth/token' 
    callback_url = callback_url
    
    def get_authenticated_user(self):
        callback = urlparse.urljoin(self.request.full_url(),self.callback_url())
        oauth_request_token_url = self._oauth_request_token_url(callback,self._oauth_consumer_token()['client_id'],self._oauth_consumer_token()['client_secret'],self.get_argument('code',None),{'grant_type':'authorization_code'})
        print oauth_request_token_url,'!!!!!!!'

    def _oauth_consumer_token(self):
        return dict(
                client_id = RENREN_CONSUMER_KEY,
                client_secret = RENREN_CONSUMER_SECRET
                )




class Www163Mixin(tornado.auth.OAuthMixin):
    _OAUTH_REQUEST_TOKEN_URL = 'http://api.t.163.com/oauth/request_token'
    _OAUTH_ACCESS_TOKEN_URL = 'http://api.t.163.com/oauth/access_token'
    _OAUTH_AUTHORIZE_URL = 'http://api.t.163.com/oauth/authenticate'
    _OAUTH_VERSION = '1.0'
    _OAUTH_NO_CALLBACKS = False
    _API_URL = 'http://api.t.163.com%s.json'

    callback_url = callback_url
    _parse_user_response = _parse_user_response
    _on_request = _on_request

    def www163_request(self, path, callback, access_token=None,
                           post_args=None, **args):
        return xxx_request(
            self, path, callback, access_token, post_args, **args
        )

    def _oauth_consumer_token(self):
        return dict(
            key=WWW163_CONSUMER_KEY,
            secret=WWW163_CONSUMER_SECRET)

    def _oauth_get_user(self, access_token, callback):
        callback = self.async_callback(self._parse_user_response, callback)
        self.www163_request(
            '/account/verify_credentials',
            access_token=access_token, callback=callback
        )


class QqMixin(tornado.auth.OAuthMixin):
    _OAUTH_REQUEST_TOKEN_URL = 'https://open.t.qq.com/cgi-bin/request_token'
    _OAUTH_ACCESS_TOKEN_URL = 'https://open.t.qq.com/cgi-bin/access_token'
    _OAUTH_AUTHORIZE_URL = 'https://open.t.qq.com/cgi-bin/authorize'
    _OAUTH_VERSION = '1.0a'
    _OAUTH_NO_CALLBACKS = False
    _API_URL = 'http://open.t.qq.com/api%s'

    callback_url = callback_url
    _parse_user_response = _parse_user_response
    _on_request = _on_request

    def _qq_request(self, path, callback, access_token=None,
                           post_args=None, **args):
        return xxx_request(
            self, path, callback, access_token, post_args, **args
        )


    def _oauth_consumer_token(self):
        return dict(
            key=QQ_CONSUMER_KEY,
            secret=QQ_CONSUMER_SECRET
        )

    def _oauth_get_user(self, access_token, callback):
        callback = self.async_callback(self._parse_user_response, callback)
        #sina_user_id = access_token['user_id']
        self._qq_request(
            '/user/info?format=json',
            access_token=access_token,
            callback=callback
        )


class SinaMixin(tornado.auth.OAuthMixin):
    _OAUTH_REQUEST_TOKEN_URL = 'http://api.t.sina.com.cn/oauth/request_token'
    _OAUTH_ACCESS_TOKEN_URL = 'http://api.t.sina.com.cn/oauth/access_token'
    _OAUTH_AUTHORIZE_URL = 'http://api.t.sina.com.cn/oauth/authorize'
    _OAUTH_VERSION = '1.0a'
    _OAUTH_NO_CALLBACKS = False
    _API_URL = 'http://api.t.sina.com.cn%s.json'

    callback_url = callback_url
    _parse_user_response = _parse_user_response
    _on_request = _on_request

    def sina_request(self, path, callback, access_token=None,
                           post_args=None, **args):
        return xxx_request(
            self, path, callback, access_token, post_args, **args
        )


    def _oauth_consumer_token(self):
        return dict(
            key=SINA_CONSUMER_KEY,
            secret=SINA_CONSUMER_SECRET)

    def _oauth_get_user(self, access_token, callback):
        callback = self.async_callback(self._parse_user_response, callback)
        sina_user_id = access_token['user_id']
        self.sina_request(
            '/users/show/%s'%sina_user_id,
            access_token=access_token, callback=callback
        )


class SohuMixin(tornado.auth.OAuthMixin):
    _OAUTH_REQUEST_TOKEN_URL = 'http://api.t.sohu.com/oauth/request_token'
    _OAUTH_ACCESS_TOKEN_URL = 'http://api.t.sohu.com/oauth/access_token'
    _OAUTH_AUTHORIZE_URL = 'http://api.t.sohu.com/oauth/authorize'
    _OAUTH_VERSION = '1.0'
    _OAUTH_NO_CALLBACKS = False
    _API_URL = 'http://api.t.sohu.com%s.json'

    callback_url = callback_url
    _parse_user_response = _parse_user_response
    _on_request = _on_request

    def sohu_request(self, path, callback, access_token=None,
                           post_args=None, **args):
        return xxx_request(
            self, path, callback, access_token, post_args, **args
        )


    def _oauth_consumer_token(self):
        return dict(
            key=SOHU_CONSUMER_KEY,
            secret=SOHU_CONSUMER_SECRET)

    def _oauth_get_user(self, access_token, callback):
        callback = self.async_callback(self._parse_user_response, callback)
        sohu_user_id = access_token['user_id']
        self.sohu_request(
            '/users/show/%s'%sohu_user_id,
            access_token=access_token, callback=callback
        )


class TwitterMixin(tornado.auth.TwitterMixin):
    callback_url = callback_url
