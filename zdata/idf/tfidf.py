#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from config import ZDATA_PATH
from zkit.tofromfile import tofile, fromfile
from idf import tf_idf as _tf_idf
from os.path import join

IDF = fromfile(join(ZDATA_PATH, "data/idf"))

def tf_idf(word_list):
    return _tf_idf(word_list, IDF)

if __name__ == "__main__":
    for k, v in tf_idf(["李开复","中国"]):
        print k,v 

