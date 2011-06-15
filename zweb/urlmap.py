#!/usr/bin/env python
#coding:utf-8

URLMAP = []

def urlmap(url, **kwds):
    def _(cls):
        URLMAP.append(
            (url, cls, kwds)
        )
        return cls
    return _


class Urlmap(object):
    def __init__(self):
        self.handlers = []

    def urlmap(self, url, **kwds):
        def _(cls):
            self.handlers.append((url, cls, kwds))
            return cls
        return _


def host_handlers(host, *args):
    handlers = []
    for i in args:
        handlers.extend(i)
    return (host, handlers)

