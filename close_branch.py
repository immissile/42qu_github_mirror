#!/usr/bin/env python
# -*- coding: utf-8 -*-
inactive = """
yup_20111018_zsite_uid      6662:873c1c3150ac (inactive)
realfex_20111014_site_read  6644:c6d356b8e6df (inactive)
realfex_20111013_site_recommend 6631:0b5992274da9 (inactive)
zuroc_20111012_site         6585:521659aa0532 (inactive)
yup_20111011_share          6551:0496f5e2d33c (inactive)
"""

inactive = inactive.strip().split("\n")
inactive = [i.split(" ",1)[0] for i in inactive]

cmd = []
for i in inactive:
    cmd.append("hg update %s;hg commit --close-branch -m close"%i)

cmd.append("hg update default")


print ";".join(cmd)
