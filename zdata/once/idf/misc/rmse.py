#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from tfidf.train.topic_bayes import TAG2ID, WORD2ID, BAYES_RANK

def rmse(num_list):
    if num_list:
        length = float(len(num_list))
        E = sum(num_list)/length
        total = 0
        li = map(lambda x: (x-E)**2,num_list)
        return sum(li)/length

def main():
    topic_count = TAG2ID.get_max_id()
    for word_id,topic_list in BAYES_RANK.iteritems():
        print WORD2ID.get_word_by_id(word_id),rmse(map(lambda x:x[1],topic_list))
    

if __name__ == '__main__':
    main()
