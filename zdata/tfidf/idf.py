#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
import os
from collections import defaultdict
from math import log
from mmseg import seg_txt
from yajl import loads
import sys;
reload(sys);
sys.setdefaultencoding('utf-8')

from os.path import join
from zkit.tofromfile import tofile, fromfile
from zdata.config import DATA_DIR

class Idf(object):
    def __init__(self):
        self._idf = defaultdict(int)
        self._count = 0

    def append(self, txt):
        for i in set(seg_txt(str(txt.lower()))):
            self._idf[i] += 1
        self._count += 1

    def idf(self):
        result = {}
        count = float(self._count)
        for k, v in self._idf.iteritems():
            result[k] = log(count/v, 2)
            '''
            idf训练中, 低于1/100w的的词直接去掉..
            '''
            if result[k] < 1/1000000.0:
                result.pop(k)
        return result

    def tofile(self, f):
        tofile(
                f, (self._count, self.idf())
              )

    def fromfile(self, f):
        self._count , self._idf = fromfile(f)


    def tf_idf(self, txt):
        tf = defaultdict(int)
        for i in seg_txt(str(txt.lower())):
            tf[i] += 1
        result = []
        for k, v in tf.iteritems():
            if k in self._idf:
                result.append((k, v*self._idf[k]))
        return result

def idf_zhihu():
    current_path = os.path.dirname(os.path.abspath(__file__))
    idf = Idf()
    idf.fromfile(join(DATA_DIR, 'idf.idf'))
    return idf


if __name__ == '__main__':
    pass

    #tf_idf_by_zhihu()
    #idf = idf_zhihu()
    #for k, v in idf.tf_idf('我不可思议是什么的人'):
    #    print k, v


#print tf_idf('我','我不可思议是什么的人')
#current_path = os.path.dirname(os.path.abspath(__file__))
#data=[]

#total_files = len(data)
#def idf_list(word_list):
#    word_idf_dict = defaultdict(int)
#
#    ##for i in data:
#    ##    ans = '\n'.join([x['answer'] for x in i['answer']])
#    ##    for word in word_list:
#    ##        if word in i['body'] or word in ans or word in i['title']:
#    ##            word_idf_dict[word]+=1
#    ##word_idf_dict = [(k,log(total_files/float(v))) for k,v in word_idf_dict.items()]
#
#    return word_idf_dict
#
##def idf(word):
##    word_idf=0
##    for i in data:
##        ans = ''.join([x['answer'] for x in i['answer']])
##        if word in i['body'] or word in ans or word in i['title']:
##            word_idf+=1
##
##    word_idf = log(total_files/float(word_idf))
##    return word_idf
#
##def tf(word,text):
##    words = list(seg_txt(text))
##    print words
##    count = text.count(word)
##    return count/float(len(words))
##
##def tf_idf(word,text):
##    return tf(word,text)*idf(word)
#

