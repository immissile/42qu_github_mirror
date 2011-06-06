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
