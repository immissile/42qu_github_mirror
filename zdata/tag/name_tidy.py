#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from name2id import NAME2ID
from zkit.pprint import pprint
from zkit.fanjian import utf8_ftoj

def name_tidy(name):
    return utf8_ftoj(str(name)).lower().replace("·"," ").replace("《","").replace("《","").split("(",1)[0]

def main():
    t = {}
    for k,v in NAME2ID.iteritems():
        t[name_tidy(k)] = v
    print "#coding: utf-8"
    print "NAME2ID = ",
    pprint(t)


if "__main__" == __name__:
    main()

