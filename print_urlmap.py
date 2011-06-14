#!/usr/bin/env python
#coding:utf-8
import pyclbr

def print_urlmap(module):
    __import__(module, globals(), locals(), [], -1)
    print '\n%s :'%module

    from pprint import pprint
    import zweb
    prefix = len(module)+1
    #pyclbr.readmodule("ctrl.index")

    for i in sorted(zweb._urlmap.URLMAP):
        url, cls = i[:2]
        mn = cls.__module__
    
        mddict = pyclbr.readmodule(mn)
        cls_name = cls.__name__
        mn = mn.replace('.', '/') +'.py'
        print '\t%s\t%s%s'%(url.ljust(42), ('%s : %s'%(mn, mddict[cls_name].lineno)).ljust(42) , cls_name )

    zweb._urlmap.URLMAP = []

print_urlmap('ctrl._urlmap')
print_urlmap('ctrl.zsite._urlmap')
print_urlmap('ctrl.main._urlmap')
print_urlmap('god._urlmap')
print_urlmap('api._urlmap')
