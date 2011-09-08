#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import string
import _env

from model.zsite import Zsite, zsite_name_rm


nums = string.digits

def check(a):
    if type(a) is not str:
        return False
    else:
        for i in a:
            if i not in nums:
                return False
        return True


def get_name():
    names = Zsite.raw_sql('select id,name from zpage.zsite').fetchall()
    for id,name in names:
        if check(name):
            zsite_name_rm(id)
    
if __name__ == "__main__":
    get_name()
