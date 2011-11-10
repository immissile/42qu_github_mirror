#!/usr/bin/env python
#coding:utf-8


branches = """
zuroc_20111108_com          7005:1fe04896e043
zuroc_20111104_com          6987:cd71e64408f3
realfex_20111101_job        6940:82cdb26bdf18 (inactive)
yup_1031_site_note          6928:3816219f8044 (inactive)
realfex_20111027_pop_hero   6872:5ad7a2956f08 (inactive)
"""

branches = branches.strip()

for i in branches.split("\n"):
    j = i.split(" ",1)[0]
    print "hg update %s ; hg commit --close-branch -m close;"%j

print "hg update default"

