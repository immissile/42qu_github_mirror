#!/usr/bin/env python
#coding:utf-8


branches = """

realfex_20111026_weekly_mail 6848:b07e0aa9185d (inactive)
realfex_20111021_hero_pop   6743:3f670d1fab80 (inactive)
zuroc_20111014_siterec      6720:1e8b8c5d064e (inactive)
yup_20111021_xiaonei        6713:7776b4c3c82e (inactive)
yup_20111017_google_contacts 6712:21251b9c0552 (inactive)
realfex_20111017_add_friends 6669:b251e1028a78 (inactive)
"""

branches = branches.strip()

for i in branches.split("\n"):
    j = i.split(" ",1)[0]
    print "hg update %s ; hg commit --close-branch -m close;"%j

print "hg update default"

