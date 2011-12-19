#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from model.zsite_list import ZsiteList
from model.zsite import Zsite
from json import loads
from model.career import Career, CID_EDU
from collections import  defaultdict
from model.user_school import user_school_json, user_school_new

user = defaultdict(list)




with open("exported") as f:
    for line in f:
        data = loads(line)
        print data[0],data[1],data[3]/10000,0,data[2],data[4]
        user_school_new(data[0],data[1],data[3]/10000,0,data[2],txt=data[4])
        raw_input()

for i in Career.where(cid=CID_EDU):
    i.unit_id = user[i.user_id][0][1]
    i.title_id = user[i.user_id][0][2]
    i.save()
    user[i.user_id].pop(0)

