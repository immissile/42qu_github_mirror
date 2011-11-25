#!/usr/bin/env python
#coding:utf-8


branches = """

zuroc_201111118_com         7525:824ba9ed30ce (inactive)
zuroc_201111123_com2        7510:87552bf8298e (inactive)
zuroc_201111123_com         7498:030a2d387eaa (inactive)
zuroc_201111110_com         7251:623e72ee290b (inactive)

"""

branches = branches.strip()

for i in branches.split('\n'):
    j = i.split(' ', 1)[0]
    print 'hg update %s ; hg commit --close-branch -m close;'%j

print 'hg update default'

