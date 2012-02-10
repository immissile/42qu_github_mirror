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

class Df(object):
    def __init__(self):
        self._df = defaultdict(int)
        self._count = 0

    def append(self, txt):
        for i in set(txt2word(txt)):
            self._df[i] += 1
        self._count += 1

    def tofile(self, f):
        tofile(
            f, (self._count, dict(self._df.iteritems()))
        )

    def fromfile(self, f):
        self._count , _df = fromfile(f)
        self._df = defaultdict(int)(_df.iteritems())


    def extend(self, other):
        self.count += other.count
        for k,v in other._df.iteritems():
            self._df[k]+=v

def df_merge(*args):
    df = Df()
    for i in args:
        df.extend(i)
    return df






if __name__ == '__main__':
    pass

