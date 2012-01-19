#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from retry import urlfetch
from pic import picopen


def fetch_pic(url, referer=None):
    headers = {}

    if referer:
        headers['Referer'] = referer

    request = urllib2.Request(url, None, headers)
    raw = urlfetch(request)

    img = picopen(raw)
    return img


