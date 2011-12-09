#!/usr/bin/env python
#coding:utf-8


branches = """

yup_20111202_addppt         7873:335d081d14ff (inactive)
zuroc_20111201_login2       7866:faf955228806 (inactive)
yup_20111130_change_mail    7799:c153a1b7e52e (inactive)
yup_20111125_product_show   7706:3bd253e2ca0b (inactive)
"""

branches = branches.strip()

for i in branches.split("\n"):
    j = i.split(" ",1)[0]
    print "hg update %s ; hg commit --close-branch -m close;"%j

print "hg update default"

