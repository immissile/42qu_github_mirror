#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from model.zsite_list import ZsiteList
from model.zsite import Zsite
from json import loads
from model.career import Career, CID_EDU
from collections import  defaultdict

user = defaultdict(list)
with open("exported") as f:
    for line in f:
        data = loads(line)
        user[data[0]].append(data)

for i in Career.where(cid=CID_EDU):
    i.unit_id = user[i.user_id][0][1]
    i.title_id = user[i.user_id][0][2]
    user[i.user_id].pop(0)

