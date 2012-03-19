#!/usr/bin/env python
#coding:utf-8

import urllib2
import traceback
import time
import sys
from urllib2 import urlopen

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
    try:
        r = urllib2.urlopen(url, data, timeout=30)
        c = r.read()
        return c
    except:
        if isinstance(url, urllib2.Request):
            print url.get_full_url()
        else:
            print url
        traceback.print_exc()

if __name__=='__main__':
    print urlfetch("http://google.com")
