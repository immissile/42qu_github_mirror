#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import time
import sys
import traceback

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
                traceback.print_exc()
        return func(*args, **kwargs)
    return _

@retry
def urlfetch(url, data=None, timeout=30):
    try:
        r = urllib2.urlopen(url, data, timeout=30)
        c = r.read()
        return c
    except:
        print url
        traceback.print_exc()

