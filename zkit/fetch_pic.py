#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from urlfetch import urlfetch
from pic import picopen


def fetch_pic(url, referer=None):
    headers = {}

    if referer:
        headers['Referer'] = referer

    request = urllib2.Request(url, None, headers)
    raw = urlfetch(request)

    img = picopen(raw)
    return img

if __name__ == '__main__':
    pass
    fetch_pic("http://27.media.tumblr.com/tumblr_ly0eyceSeo1qigppz_1326962065_cover.jpg")
    
