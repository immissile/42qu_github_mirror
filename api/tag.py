#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from model._db import redis 

def tag_from_zset(name):
    pass

def tag_from_trie(name):
    pass

def tag_new(tag_name):
    for sub_tag in tag_name.split("/"):
        sub_tag = str(sub_tag)
        for pos in xrange(len(sub_tag)):
            print sub_tag[:pos]

if __name__ == '__main__':
    tag_new("史蒂夫/乔布斯/steve/jobs")

