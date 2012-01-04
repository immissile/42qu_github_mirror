#!/usr/bin/env python
# -*- coding: utf-8 -*-
from yajl import loads, dumps
from collections import defaultdict
from mmseg import seg_txt
import os
from os.path import join, dirname
from tofromfile import tofile, fromfile
from find_parent_tag import ParentTagger

current_path = os.path.dirname(os.path.abspath(__file__))

class WordId(object):
    def __init__(self):
        self._dict = {}
    
    def word_to_id(self):
        return self._dict

    def get_id_by_tag(self,tag):
        if tag in self._dict:
            return _dict[tag]
        return None

    def id_by_tag(self, tag):
        tag = str(tag)
        _dict = self._dict
        if tag in _dict:
            return _dict[tag]
        id = len(_dict)+1
        _dict[tag] = id
        return id

    def tofile(self, path):
        tofile(path, self._dict)

    def fromfile(self, path):
        self._dict = fromfile(path)
        return self

    def id_list_by_word_list(self, tag_list):
        result = []
        for i in tag_list:
            result.append(self.id_by_tag(i))
        return result

    def id2word(self):
        return dict((k,v) for v,k in self._dict.iteritems())

class TagWord(object):
    def __init__(self, path):
        self.tag2id = WordId()
        self.word2id = WordId()
        self.path = path
        self.parent_tag_finder = ParentTagger()

    def _txt_tag_generator(self):
        path = self.path
        tag2id = self.tag2id
        with open(path) as f:
            for line in f:
                data = loads(line)
                tags = data['tags']
                '''
                查找上级标签
                '''
                parent_list = self.parent_tag_finder.get_parent_tag_list_by_list(tags)
                tags.extend(parent_list)
                id_list = tag2id.id_list_by_word_list(tags)
                yield data['title'], id_list
                for ans in data['answer']:
                    yield ans['answer'], id_list
                '''
                训练时, 将主题也算作一个词来处理.
                '''
                for tag in tags:
                    yield tag,id_list

    def txt_tag_generator(self):
        word2id = self.word2id
        for k, v in self._txt_tag_generator():
            words = list(seg_txt(str(k).lower()))
            yield word2id.id_list_by_word_list(words) , v

    def tofile(self):
        word_id2tag_id = list(self.txt_tag_generator())
        path = dirname(self.path)
        self.tag2id.tofile(join(path, 'tag2id'))
        self.word2id.tofile(join(path, 'word2id'))
        tofile(join(path, 'word_id2tag_id'), word_id2tag_id)

def word_tag_word2tag_fromfile( path):
    return map(fromfile,
                map(
                    lambda x:join(path, x),
                    ('tag2id', 'word2id')
                )
            )


class BayesRank(object):
    def __init__(self, word_id2tag_id):
        topic_id_title_count = self.topic_id_title_count = defaultdict(int)
        word_topic_count = self.word_topic_count = defaultdict(lambda:defaultdict(int))

        for word_id_list, tag_id_list in word_id2tag_id:
            for tag_id in tag_id_list:
                topic_id_title_count[tag_id] += 1
                for word_id in word_id_list:
                    word_topic_count[word_id][tag_id] += 1

    def rank(self):
        topic_id_title_count = self.topic_id_title_count
        word_topic_count = self.word_topic_count

        word_topic_bayes = {}
        for word, topic_count in word_topic_count.iteritems():
            word_topic_freq = {}
            for topic_id, count in topic_count.iteritems():
                topic2title = topic_id_title_count[topic_id]
                if topic2title<20:
                    continue
                word_topic_freq[topic_id] = count/float(topic2title)

            count = sum(word_topic_freq.itervalues())
            wb = word_topic_bayes[word] = []
            for k, v in word_topic_freq.iteritems():
                wb.append((k, v/count))
        return word_topic_bayes

def main():
    tagword=TagWord("data/out.js")
    tagword.tofile()
    WORD_ID2TAG_ID = fromfile( "data/word_id2tag_id")
    bayes_rank = BayesRank(WORD_ID2TAG_ID)
    tofile( "data/bayes_rank" , bayes_rank.rank())

if __name__ == '__main__':
    main()
else:
    BAYES_RANK = fromfile(join(current_path, "data/bayes_rank"))
    TAG2ID = WordId().fromfile(join(current_path, 'data/tag2id'))
    WORD2ID = WordId().fromfile(join(current_path, 'data/word2id'))
