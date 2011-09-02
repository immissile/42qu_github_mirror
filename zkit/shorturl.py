#!/usr/bin/env python
#coding:utf-8
import urllib
import urllib2
from urllib2 import urlopen
import httplib
from yajl import loads
import traceback
import time
import sys

SINA_API_KEY = '3152496704'

SINA_SHORT_URL = 'http://api.t.sina.com.cn/short_url/shorten.json?source=%s&url_long=%%s'%SINA_API_KEY

def retry(func):
    def _(*args, **kwargs):
        tries = 2
        while tries:
            try:
                return func(*args, **kwargs)
            except urllib2.HTTPError, e:
                if e.getcode() == 404:
                    return
            except :
                time.sleep(0.1)
                tries -= 1
                sys.stdout.flush()
                traceback.print_exc()
        return func(*args, **kwargs)
    return _


@retry
def urlfetch(url, data=None):
    r = urlopen(url, data, timeout=30)
    c = r.read()
    return c

def t_cn(url):
    url = urllib.quote(url)
    url = SINA_SHORT_URL%url
    result = urlfetch(url)
    result = loads(result)
    return result[0]['url_short']


def dwz_cn(url):
    url = urllib.quote(url)
    print url
    result = urlfetch('http://dwz.cn/create.php', data='url=%s'%url)
    result = loads(result)
    if 'err_msg' in result:
        print result['err_msg']
    else:
        return result['tinyurl']

if '__main__' == __name__:
    url = 'http://42qu.com/1233?1'
    print dwz_cn(url)

