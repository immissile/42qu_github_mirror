#!/usr/bin/env python
#coding:utf-8

class StrCls(object):
    def __init__(self, o):
        self.__o__ = o

    def __iter__(self):
        for i in self.__d.iteritems():
            yield i

    def __nonzero__(self):
        return bool(self.__d)

    def __setattr__(self, name, val):
        if val is not None:
            self.__d[name] = val

    def __getattr__(self, name):
        return self.__d.get(name, "")

    def __getitem__(self, name):
        return self.__d.get(name, "")

    def __contains__(self, b):
        return b in self.__d

    def __setitem__(self, name, val):
        if val is not None:
            self.__d[name] = val

    def __delitem__(self, name):
        del self.__d[name]


