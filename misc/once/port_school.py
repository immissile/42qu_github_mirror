#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from model.zsite_list import ZsiteList
from model.zsite import Zsite

from model.career import Career, CID_EDU

for i in Career.where(cid=CID_EDU):
    print i
