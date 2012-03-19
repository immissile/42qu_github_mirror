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
import ctrl._url_istarsea



print_urlmap('ctrl._urlmap_istarsea.i')
print_urlmap('ctrl._urlmap_istarsea.istarsea')
print_urlmap('ctrl._urlmap_istarsea.j')
