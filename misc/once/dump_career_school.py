#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from model.zsite_list import ZsiteList
from model.zsite import Zsite
from json import loads, dumps
from model.career import Career, CID_EDU
from collections import  defaultdict
from model.user_school import user_school_json, user_school_new
user = defaultdict(list)




for pos, i in enumerate(Career.where(cid=CID_EDU)):
    result = {}
    for j in i._fields:
        result[j] = getattr(i, j)

    print dumps(result)
