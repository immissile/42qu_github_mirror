#!/usr/bin/env python
#coding:utf-8


branches = """
zuroc_20111108_com          7005:1fe04896e043
yup_20111101_com            7037:22dede514031 (inactive)
"""

branches = branches.strip()

for i in branches.split("\n"):
    j = i.split(" ",1)[0]
    print "hg update %s ; hg commit --close-branch -m close;"%j

print "hg update default"

