#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from itertools import tee, izip
from array import array
import sys
import os.path as path
from kyotocabinet import *
from zdata.config import KYOTO_DB_PATH

MAX_INT = (1<<32)-1

class DbKyoto(object):
    def __init__(self, db_file):
        #from train import TAG2ID, WORD2ID#, BAYES_RANK
        #self.ider = WORD2ID
        self.db = DB()
        self.db_file = db_file
        print path.join(KYOTO_DB_PATH,self.db_file)
        if not self.db.open(path.join(KYOTO_DB_PATH,self.db_file), DB.OWRITER | DB.OCREATE):
            print >>sys.stderr, "open error: " + str(self.db.error())

    def set(self,entry):
        key = entry[0]
        result_array = convert2array(entry[1]).tostring()
        if not self.db.set(key,result_array):
            print key
            print result_array
            print >>sys.stderr, "open error: " + str(self.db.error())

    def get(self,key):
        value = self.db.get(key)
        if value:
            result = array('L')
            result.fromstring(value)
            return convert2dict(result)
        else:
            #print >>sys.stderr, self.ider.get_word_by_id(key)
            #print key
            #print >>sys.stderr, "%s error: "%key + str(self.db.error())
            pass

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

#for k,v in pairwise(range(10)):
#    print k,v

def convert2array(dict_value):
    ''' 
    >>> convert2array({1:0.1,2:0.3})
    array('L', [1L, 429496729L, 2L, 1288490188L])
    '''
    result_list =  []  
    for k,v in dict_value:
        result_list.extend([k,int(v*MAX_INT)])
    result = array('L',result_list)
    return result

def convert2dict(array_l):
    ''' 
    >>> convert2dict([1L, 429496729L, 2L, 1288490188L])
    {1:0.1,2:0.3}
    '''
    return [ (array_l[i],array_l[i+1]) for i in range(len(array_l)) if i%2==0]

if __name__=='__main__':
    #import doctest
    #doctest.testmod()
    from kyotocabinet import DB
    db = DB()
    db.open('/mnt/zdata/kyoto/kyoto.kch', DB.OREADER)
    print db.get(15439)
