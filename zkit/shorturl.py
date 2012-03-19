#!/usr/bin/env python
#coding:utf-8
import urllib
import urllib2
from urllib2 import urlopen
from yajl import loads
import traceback
import sys
from urllib import  urlencode
from urlfetch import urlfetch

SINA_API_KEY = '3152496704'

SINA_SHORT_URL = 'http://api.t.sina.com.cn/short_url/shorten.json?source=%s&url_long=%%s'%SINA_API_KEY

def t_cn(url):
    url = urllib.quote(url)
    url = SINA_SHORT_URL%url
    result = urlfetch(url)
    result = loads(result)
    return result[0]['url_short']


def dwz_cn(url):
    url = urllib.quote(url)
    result = urlfetch('http://dwz.cn/create.php', data='url=%s'%url)
    result = loads(result)
    if 'err_msg' in result:
        print result['err_msg']
    else:
        return result['tinyurl']

def curt_cc(url):
    _url = url
    url = urllib.quote(url)
    result = urlfetch('http://curt.cc/service/generator.php?url=%s'%url)
    try:
        result = loads(result)
        return result['url']
    except:
        traceback.print_exc()
        return _url

def xrl_us(url):
    _url = url
    url = urllib.quote(url)
    try:
        result = urlopen(
            'http://metamark.net/api/rest/simple',
            urlencode({'long_url':url})
        ).read()
        return result
    except:
        traceback.print_exc()
        return _url

if '__main__' == __name__:
    url = 'http://42qu.com/1233?122234'
    print xrl_us(url)
    #print curt_cc(url)
    #print t_cn(url)
