#coding:utf-8
import _env
from config import ZDATA_PATH
from ptag import PTAG
from mmseg import seg_txt
from collections import defaultdict
from zkit import tofromfile
from math import log
from zkit.pprint import pprint
from os.path import basename, join, exists
from glob import glob
from name2id import NAME2ID
from name_tidy import name_tidy
from yajl import dumps
CACHE_PATH = "/mnt/zdata/train/tag"

def train(filename, parser):
    fname = basename(filename)
    cache_path = join(CACHE_PATH, fname)
    if exists(cache_path):
        return

    word2tag_count = {}
    for tag_id_list, txt in parser(filename):
        if not txt.strip():
            continue

        tag_id_set = set(tag_id_list)
        if not tag_id_set:
            continue

        for tid in tuple(tag_id_set):
            tag_id_set.update(PTAG.get(tid, ()))

        word2count = defaultdict(int)
        word_list = list(seg_txt(str(txt)))
        for i in word_list:
            word2count[i] += 1

        for k, v in word2count.iteritems():
            if k not in word2tag_count:
                word2tag_count[k] = {}
            t = word2tag_count[k]
            for id in tag_id_set:
                if id not in t:
                    t[id] = 0
                t[id] += (1+log(float(v)))

    tofromfile.tofile(cache_path, word2tag_count)

def merge():
    CACHE_PATH = "/home/work/wanfang/tag"
    for pos, i in enumerate(glob(CACHE_PATH+"/*")):
        for word, topic_freq in tofromfile.fromfile(i).iteritems():

            if len(word.strip()) <= 3:
                continue

            word = name_tidy(word)
            s = [word]
            for topic, freq in topic_freq.iteritems():
                topic = int(topic)
                s.append((topic, freq))
            print dumps(s)

#                if topic not in db:
#                    topic_word_count[topic] = 0
#                topic_word_count[topic] += freq
                #print topic, freq
#                word_topic_freq[word][topic] += freq

#        if pos>3:
#            break

#    total = sum(topic_word_count.itervalues())
#
#    for word, topic_freq in word_topic_freq.iteritems():
#        if word in NAME2ID:
#            tid = NAME2ID[word]
#            now = topic_freq[tid]
#            topic_freq[tid] = new = sum(topic_freq.itervalues()) 
#            topic_word_count[tid]+=(new-now)
#            total += new-now
#
#    for word, topic_freq in word_topic_freq.iteritems():
#        tf = []
#        
#        ftotal = 0.0
#        for topic, freq in topic_freq.iteritems():
#            f = freq*10000/topic_word_count[topic]
#            tf.append((topic, f))
#            ftotal += f
#        
#        tf = [(k,v/ftotal) for k,v in tf]
#
#        print dumps((word, tf))    



if __name__ == "__main__":
    merge()

#    path = join(ZDATA_PATH_TRAIN_IDF, filename)
#
#    tofile = "%s.idf"%path
#    if exists(tofile):
#        #cmd = 'scp %s work@stdyun.com:%s'%(tofile, tofile)
#        #print cmd
#        #r = envoy.run(cmd)
#        #print r.std_out
#        return
#
#    if not exists(path):
#        return
#
#    df = Df()
#    count = 0
#    with open(path) as f:
#        for txt in parser(f):
#            df.append(txt)
#            if count%1000 == 1:
#                print filename, count
#            count += 1
#
#    df.tofile(tofile)
