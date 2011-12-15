#!/usr/bin/env python
#coding:utf-8


branches = """
wooparadog_20111215_feed_new
wooparadog_20111215_feed_new2
"""

branches = branches.strip()

for i in branches.split('\n'):
    j = i.split(' ', 1)[0]
    print 'hg update %s ; hg commit --close-branch -m close;'%j

print 'hg update default'

