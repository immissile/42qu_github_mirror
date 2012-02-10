#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from math import log
from zkit.tofromfile import tofile, fromfile
from collections import defaultdict

def idf_dumps(count, df):
    result = {}
    count = float(count)
    for k, v in df.iteritems():
        rank = count/v
        if rank > 1000000: # idf训练中, 低于1/100w的的词直接去掉..
            continue
        result[k] = log(rank)

    return result

def tf_idf(word_list, idf):
    tf = defaultdict(int)
    for i in word_list:
        tf[i] += 1
    result = []
   
    s = float(sum(i**2 for i in tf.itervalues()))

    for k, v in tf.iteritems():
        if k in idf:
            result.append((k, v/s*idf[k]))

    return result
