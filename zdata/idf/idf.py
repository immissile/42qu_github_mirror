#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
import os
from collections import defaultdict
from math import log
from mmseg import seg_txt
from yajl import loads

from os.path import join
from zkit.tofromfile import tofile, fromfile
from config import ZDATA_PATH
from zkit.fanjian import utf8_ftoj

def txt2word(txt):
    return seg_txt(
        utf8_ftoj(str(txt.lower()))
    )

class Idf(object):
    def __init__(self):
        self._idf = defaultdict(int)
        self._count = 0

    def append(self, txt):
        for i in set(txt2word):
            self._idf[i] += 1
        self._count += 1

    def dumps(self):
        result = {}
        count = float(self._count)
        for k, v in self._idf.iteritems():
            rank = count/v
            if rank > 1000000: # idf训练中, 低于1/100w的的词直接去掉..
                continue
            result[k] = log(rank)
        return result

    def tofile(self, f):
        tofile(
            f, (self._count, self.dumps())
        )

    def fromfile(self, f):
        self._count , self._idf = fromfile(f)


    def tf_idf(self, txt):
        tf = defaultdict(int)
        for i in txt2word(txt):
            tf[i] += 1
        result = []
        for k, v in tf.iteritems():
            if k in self._idf:
                result.append((k, v*self._idf[k]))
        return result



if __name__ == '__main__':
    pass

