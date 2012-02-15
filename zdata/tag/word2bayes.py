#coding:utf-8
import _env
from config import ZDATA_PATH
from collections import defaultdict
from name2id import NAME2ID
import glob
from config import REDIS_CONFIG
import redis

REDIS_CONFIG['db']=1
redis = redis.Redis(**REDIS_CONFIG)


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
