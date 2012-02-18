#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from collections import defaultdict

topic_freq_count = defaultdict(int)

with open("freq/w2.txt") as freq:
    for line in freq:
        line = line.strip()
        topic , freq , word = line.split(" ",2)
        topic = int(topic)
        freq = int(freq)
        #print topic, freq, word
        topic_freq_count[topic] += freq



with open("freq/w2.txt") as freq:
    for line in freq:
        line = line.strip()
        topic , freq , word = line.split(" ",2)
        topic = int(topic)
        count = topic_freq_count[topic]
        if count < 10000:
            continue
        freq = freq*500000/count
        if freq > 0:
            print topic, freq, word

def main():
    pass


if "__main__" == __name__:
    main()

