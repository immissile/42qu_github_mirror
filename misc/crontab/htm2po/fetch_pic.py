#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from zkit.retry import urlfetch
from zkit.pic import picopen

def fetch_pic(url, referer=None):
    if referer is None:
        referer = 'https://www.google.com/reader/'

    request = urllib2.Request(url, None, {'Referer': referer})
    raw = urlfetch(request)
    return picopen(raw)


def main():
    fetch_pic('http://static9.photo.sina.com.cn/middle/4860bdb2g760bced6c288&amp;690')


if '__main__' == __name__:
    main()
