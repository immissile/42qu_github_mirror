#!/usr/bin/env python
#coding:utf-8

def print_urlmap(module):
    __import__(module, globals(), locals(), [], -1)
    print '\n%s :'%module

    from pprint import pprint
    import zweb
    prefix = len(module)+1
    premn = None
    for i in sorted(zweb._urlmap.URLMAP):
        url, cls = i[:2]
        mn = cls.__module__
        if mn.startswith(module):    
            mn = mn[prefix:]
        mn = mn +'.py'
        if mn == premn:
            mn = ''
        else:
            premn = mn
        print '\t%s\t%s%s'%(url.ljust(24), '%s'%(mn).ljust(16) , cls.__name__)

    zweb._urlmap.URLMAP = []

print_urlmap('ctrl.zsite')
print_urlmap('ctrl.main')
print_urlmap('god')
print_urlmap('api')
