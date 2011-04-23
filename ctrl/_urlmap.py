#!/usr/bin/env python
#coding:utf-8

URLMAP = []

def urlmap(url):
    def _(cls):
        URLMAP.append((url, cls))
        return cls
    return _
