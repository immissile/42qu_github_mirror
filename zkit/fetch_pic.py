#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from urlfetch import urlfetch
from pic import picopen
from urlparse import urlparse


def fetch_pic(url, referer=None):
    headers = {}

    parts = urlparse(url)

    if referer:
        headers['Referer'] = referer
    else:
        if "sina" in url:
            headers['Referer'] = 'http://blog.sina.com.cn/'
        else:
            headers['Referer'] = 'http://%s'%parts[1]

    request = urllib2.Request(url, None, headers)
    raw = urlfetch(request)

    img = picopen(raw)
    return img

if __name__ == '__main__':
    pass
    fetch_pic("http://27.media.tumblr.com/tumblr_ly0eyceSeo1qigppz_1326962065_cover.jpg")
    
