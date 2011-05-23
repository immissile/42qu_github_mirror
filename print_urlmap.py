#!/usr/bin/env python
#coding:utf-8
import ctrl

def print_urlmap(module):
    __import__(module, globals(), locals(), [], -1)
    print ""
    print (" %s "%module).center(72, "=")

    from pprint import pprint
    import zweb

    for url, cls in sorted(zweb._urlmap.URLMAP):
        print "%s\t%s.%s"%(url.ljust(32), cls.__module__,cls.__name__)

    zweb._urlmap.URLMAP = []

print_urlmap("ctrl")
print_urlmap("god")
