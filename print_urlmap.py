#!/usr/bin/env python
#coding:utf-8
import pyclbr

def print_urlmap(module):
    mod = __import__(module, globals(), locals(), ['_urlmap'], -1)
    print '\n%s :'%module
    from pprint import pprint
    import zweb
    prefix = len(module)+1
    #pyclbr.readmodule("ctrl.index")

    for i in sorted(mod._urlmap.urlmap.handlers):
        url, cls = i[:2]
        mn = cls.__module__

        mddict = pyclbr.readmodule(mn)
        cls_name = cls.__name__
        mn = mn.replace('.', '/') +'.py'
        print '\t%s\t%s%s'%(
            ('%s +%s;'%(mn, mddict[cls_name].lineno)).ljust(42),
            url.ljust(42),
            cls_name
        )

from ctrl import _url
print_urlmap('ctrl.j')
print_urlmap('ctrl.zsite')
print_urlmap('ctrl.main')
#print_urlmap('god._urlmap')
#print_urlmap('api._urlmap')

