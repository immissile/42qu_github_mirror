#!/usr/bin/env python
#coding:utf-8


branches = """

wooparadog_20111230_buzz_at 8923:b38286e7ca40 (inactive)
zuroc_20111226_newindex     8844:e205848bf33c (inactive)
zuroc_201123_newindex       8641:02418b868976 (inactive)
wooparadog_20111215_feed_new3 8619:33101b506935 (inactive)
wooparadog_20111219_new_buzz 8561:43b6a8309596 (inactive)
"""


for i in branches.strip().split('\n'):
    j = i.split(' ', 1)[0]
    print 'hg update %s ; hg commit --close-branch -m close;'%j

print 'hg update default'

