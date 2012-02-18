#coding:utf-8
import _env
from config import ZDATA_PATH
from collections import defaultdict
from name2id import NAME2ID
from glob import glob
from config import REDIS_CONFIG
import redis
from zkit import tofromfile
from name_tidy import name_tidy
from yajl import dumps
from zkit.zitertools import chunkiter
from collections import defaultdict

REDIS_CONFIG['db']=1
redis = redis.Redis(**REDIS_CONFIG)


def merge():
    topic_count = defaultdict(int)

    f = "word2count.txt"

    with open(f,"w") as word2freq:
        for key in redis.keys("*"):
            l = redis.hgetall(key)
            for k,v in l.iteritems():
                topic_count[int(k)]+=int(v)
                word2freq.write("%s %s %s\n"%(k,v,key))

    with open(f) as freq:
        with open("topic_freq_word.txt", "w") as topic_freq_word:
            for line in freq:
                line = line.strip()
                topic , freq , word = line.split(" ",2)
                topic = int(topic)
                count = topic_freq_count[topic]
                if count < 10000:
                    continue
                freq = int(freq)*500000/count
                if freq > 0:
#                    print topic, freq, word
                    topic_freq_word.write("%s %s %s\n"%(topic, freq, word))



if __name__ == "__main__":
    merge()
