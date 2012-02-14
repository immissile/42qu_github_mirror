#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from math import log
from zkit.tofromfile import tofile, fromfile
from collections import defaultdict
from operator import itemgetter

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

    total = len(word_list)
    for k, v in tf.iteritems():
        if k in idf:
            v = 1+log(v)
            #print k, v,  idf[k] ,"---------"
            result.append((k, v*idf[k]))

    total = sum(i[1]**2 for i in result)**.5
    result = [(i[0], i[1]/total) for i in result]
    result.sort(key=itemgetter(1), reverse=True)
    return result
