#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from model.career import Career
from collections import  defaultdict
from model.user_school import user_school_json

user = defaultdict(list)


for i in Career.where():
    if i.unit == "单位":
        print i.unit , i.title, i.id
        if i.title=="头衔":
            i.delete()

#with open("exported2") as f:
#    for line in f:
#        data = loads(line)
#        print data[0],data[1],int(data[3]/10000),0,data[2],data[4]
#        user_school_new(data[0],data[1],int(data[3]/10000),0,data[2],txt=data[4])
#        Career.where(cid=CID_EDU,user_id=data[0]).delete()

#for i in Career.where(cid=CID_EDU):
#    i.unit_id = user[i.user_id][0][1]
#    i.title_id = user[i.user_id][0][2]
#    i.save()
#    user[i.user_id].pop(0)

