#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from zkit.tofromfile import tofile, fromfile

def idf_dumps(filename, count, df):
    result = {}
    count = float(self._count)
    for k, v in idf.iteritems():
        rank = count/v
        if rank > 1000000: # idf训练中, 低于1/100w的的词直接去掉..
            continue
        result[k] = log(rank)
    return result


def tf_idf(idf, word_list):
    tf = defaultdict(int)
    for i in word_list:
        tf[i] += 1
    result = []
    for k, v in tf.iteritems():
        if k in self._idf:
            result.append((k, v*idf[k]))
    return result
