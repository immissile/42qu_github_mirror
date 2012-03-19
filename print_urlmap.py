#!/usr/bin/env python
#coding:utf-8
import pyclbr
from os.path import isdir

def print_urlmap(module):
    mod = __import__(module, globals(), locals(), ['_urlmap'], -1)
    print '\n%s :' % module.replace('._urlmap', '')
    prefix = len(module) + 1

    for i in sorted(mod.urlmap.handlers):
        url, cls = i[:2]
        mn = cls.__module__

        mddict = pyclbr.readmodule(mn)
        cls_name = cls.__name__

        mn = mn.replace('.', '/')
        if isdir(mn):
            mn += '/__init__'
        mn += '.py'

        print '\t%s\t%s%s'%(
            ('%s +%s;'%(mn, mddict[cls_name].lineno)).ljust(42),
            url.ljust(42),
            cls_name
        )


import ctrl._url_zpage
print_urlmap('ctrl._urlmap.main')
print_urlmap('ctrl._urlmap.hero')
print_urlmap('ctrl._urlmap.auth')
print_urlmap('ctrl._urlmap.j')
print_urlmap('ctrl._urlmap.zsite')
print_urlmap('ctrl._urlmap.site')
print_urlmap('ctrl._urlmap.me')
print_urlmap('ctrl._urlmap.meet')
import god._url
print_urlmap('god._urlmap')

import api._url
print_urlmap('api._urlmap')

import rpc._url
print_urlmap('rpc._urlmap')


