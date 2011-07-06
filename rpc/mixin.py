#!/usr/bin/env python
#coding:utf-8
import tornado.auth
from tornado import escape
from urllib import quote
import urllib
from tornado import httpclient
import logging
import json
from config import DOUBAN_CONSUMER_KEY, DOUBAN_CONSUMER_SECRET

def callback_url(self):
    redirect_url = self.get_argument("path", None)
    path = self.request.path
    if redirect_url:
        if redirect_url[0] != "/":
            redirect_url = "/"+redirect_url
        path = path + "?path=%s"%quote(redirect_url)
    return path


def xxx_request(self, path, callback, access_token=None, post_args=None, **args):
    url = self._API_URL%path
    if access_token:
        all_args = {}
        all_args.update(args)
        all_args.update(post_args or {})
        consumer_token = self._oauth_consumer_token()
        method = "POST" if post_args is not None else "GET"
        oauth = self._oauth_request_parameters(
            url, access_token, all_args, method=method)
        args.update(oauth)
    if args: url += "?" + urllib.urlencode(args)
    callback = self.async_callback(self._on_request, callback)
    http = httpclient.AsyncHTTPClient()
    if post_args is not None:
        http.fetch(url, method="POST", body=urllib.urlencode(post_args),
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
        logging.warning("Error response %s fetching %s", response.error,
                        response.request.url)
        callback(None)
        return
    callback(response.body)


class DoubanMixin(tornado.auth.OAuthMixin):
    _OAUTH_REQUEST_TOKEN_URL = "http://www.douban.com/service/auth/request_token"
    _OAUTH_ACCESS_TOKEN_URL = "http://www.douban.com/service/auth/access_token"
    _OAUTH_AUTHORIZE_URL = "http://www.douban.com/service/auth/authorize"
    _OAUTH_VERSION = "1.0"
    _OAUTH_NO_CALLBACKS = False
    _on_request = _on_request
    callback_url = callback_url
    def douban_request(self, path, callback, access_token=None,
                           post_args=None, **args):
        # Add the OAuth resource request signature if we have credentials
        url = "http://api.douban.com%s"%path
        if access_token:
            all_args = {}
            all_args.update(args)
            all_args.update(post_args or {})
            consumer_token = self._oauth_consumer_token()
            method = "POST" if post_args is not None else "GET"
            oauth = self._oauth_request_parameters(
                url, access_token, all_args, method=method)
            args.update(oauth)
        if args: url += "?" + urllib.urlencode(args)
        callback = self.async_callback(self._on_request, callback)
        http = httpclient.AsyncHTTPClient()
        if post_args is not None:
            http.fetch(url, method="POST", body=urllib.urlencode(post_args),
                       callback=callback)
        else:
            http.fetch(url, callback=callback)


    def _oauth_consumer_token(self):
        return dict(
            key= DOUBAN_CONSUMER_KEY,
            secret= DOUBAN_CONSUMER_SECRET)

    def _oauth_get_user(self, access_token, callback):
        callback = self.async_callback(self._parse_user_response, callback)
        douban_user_id = access_token['douban_user_id']
        self.douban_request(
            "/people/%s"%douban_user_id,
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
