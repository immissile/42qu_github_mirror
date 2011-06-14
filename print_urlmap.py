#!/usr/bin/env python
#coding:utf-8

def print_urlmap(module):
    __import__(module, globals(), locals(), [], -1)
    print '\n%s :'%module

    from pprint import pprint
    import zweb
    prefix = len(module)+1
    for i in sorted(zweb._urlmap.URLMAP):
        url, cls = i[:2]
        mn = cls.__module__
        mn = mn.replace(".","/") +'.py'
        print '\t%s\t%s%s'%(url.ljust(32), '%s'%(mn).ljust(32) , cls.__name__)

    zweb._urlmap.URLMAP = []

print_urlmap('ctrl._urlmap')
print_urlmap('ctrl.zsite._urlmap')
print_urlmap('ctrl.main._urlmap')
print_urlmap('god')
print_urlmap('api')
