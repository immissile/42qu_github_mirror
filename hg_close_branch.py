#!/usr/bin/env python
#coding:utf-8


branches = """
wooparadog_20111207_recommend_post 8080:94b7f5a9d5f5 (inactive)
zuroc_20111209_newbie       8010:abec2214e9a8 (inactive)
"""

branches = branches.strip()

for i in branches.split('\n'):
    j = i.split(' ', 1)[0]
    print 'hg update %s ; hg commit --close-branch -m close;'%j

print 'hg update default'

