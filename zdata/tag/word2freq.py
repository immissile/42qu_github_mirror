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

    keys = redis.keys("*")
    for pos, key in enumerate(keys):
        l = redis.hgetall(key)
        print "1",pos, key
        for k,v in l.iteritems():
            topic_count[int(k)]+=int(v)

    #word_topic_freq = defaultdict(list)

    with open("word_tf.txt", "w") as word_freq:
        for pos, word in enumerate(keys):
            tf = []
            l = redis.hgetall(word)
            for topic, freq in l.iteritems():
                topic = int(topic)
                count = topic_count[topic]
                if count < 10000:
                    continue
                freq = int(freq)*500000/count
                if freq > 0:
                    tf.append((topic, freq))

            fcount = sum(i[1] for i in tf)

            tf = dict(tf)
            id = NAME2ID.get(name_tidy(word), 0)
            if id:
                t = tf.get(id,0)
                diff = fcount - t
                tf[id] = fcount
                fcount += diff

            if not fcount:
                continue

            t = []
            for topic, f in tf.iteritems():
                rank = int(f*10000/fcount)
                if rank:
                    t.append((topic, rank))
            if t:
                word_freq.write(
                    dumps([word, t])+"\n"
                )




if __name__ == "__main__":
    merge()
