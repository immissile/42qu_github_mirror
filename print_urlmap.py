#!/usr/bin/env python
#coding:utf-8

def print_urlmap(module):
    __import__(module, globals(), locals(), [], -1)
    print "\n%s :"%module

    from pprint import pprint
    import zweb
    prefix = len(module)+1
    premn = None
    for url, cls in sorted(zweb._urlmap.URLMAP):
        mn = cls.__module__[prefix:]+".py"
        if mn == premn:
            mn = ""
        else:
            premn = mn
        print "\t%s\t%s%s"%(url.ljust(24), "%s"%(mn).ljust(16) , cls.__name__)

    zweb._urlmap.URLMAP = []

print_urlmap("ctrl")
print_urlmap("god")
