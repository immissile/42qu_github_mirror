#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from yajl import loads, dumps
from collections import defaultdict
from glob import glob
from mmseg import seg_txt
import os
from os.path import join, dirname
from zkit.tofromfile import tofile, fromfile

from parent_tag import ParentTagger
from zdata.config import DATA_DIR
from kyoto_db import DB_Kyoto

current_path = os.path.dirname(os.path.abspath(__file__))
TAG_MAPPING = open(join(current_path, 'mapping.py'), 'w')

banned_tag_list = ['开放课程']
WORD_DOC_COUNT = defaultdict(int)

class WordId(object):
    def __init__(self):
        self._dict = {}
        self._id2word_dict = {}
        self._word_doc_count = defaultdict(int)

    def word_to_id(self):
        return self._dict

    def get_id_by_tag(self, tag):
        if tag in self._dict:
            return self._dict[tag]
        return None

    def id_by_tag(self, tag):
        if u'（' in tag:
            tag = tag[:tag.find(u'（')]
        if u'(' in tag:
            tag = tag[:tag.find(u'(')]
        lower = tag.lower()

        if tag != lower:
            print >> TAG_MAPPING, lower, ":", tag
            tag = lower

        tag = str(tag)
        _dict = self._dict
        if tag in _dict:
            return _dict[tag]

        id = len(_dict)+1
        _dict[tag] = id
        WORD_DOC_COUNT[id] += 1
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

    def _reverse_dict(self):
        if not self._id2word_dict:
            self._id2word_dict = dict((k, v) for v, k in self._dict.iteritems())

    def id2word(self):
        self._reverse_dict()
        return self._id2word_dict

    def get_word_by_id(self, id):
        self._reverse_dict()
        if id in self._id2word_dict:
            return self._id2word_dict[id]
        return None

    def get_max_id(self):
        self._reverse_dict()
        return max(self._id2word_dict.keys())


#def word2id(self):
#    return self._dict

class TagWord(object):
    def __init__(self, path):
        print "Loding"
        self.tag2id = WordId()
        self.word2id = WordId()
        self.path = path
        self.parent_tag_finder = ParentTagger()
        print "Loading done"

    def _txt_tag_generator(self):
        path = self.path
        tag2id = self.tag2id
        data_files = glob(join(path, '*.data'))
        zhihu_data = [join(path, 'zhihu')]
        zhihu_data.extend(data_files)


        print 'Processing...'
        g = open(join(path, 'topic_dict'))
        topic_dict = loads(g.read())

        count = 0
        for data_src in zhihu_data:
            print 'Processing...', data_src
            with open(data_src) as f:
                for line in f:
                    #if count > 1000:
                    #    break
                    #count += 1
                    data = loads(line)
                    if 'tags' in data:
                        tags = data['tags']
                    else:
                        continue


                    tags_processed = []
                    if 'zhihu' not in data_src:
                        for tag in tags:
                            if tag in topic_dict and tag not in banned_tag_list:
                                tags_processed.append(tag)

                        if not tags_processed:
                            continue
                        else:
                            tags = tags_processed
                            #print tags
                            #raw_input()
                    '''
                    查找上级标签
                    '''
                    parent_list = self.parent_tag_finder.get_parent_tag_list_by_list(tags)
                    tags.extend(parent_list)
                    id_list = tag2id.id_list_by_word_list(tags)
                    yield data['txt'], id_list

    def txt_tag_generator(self):
        word2id = self.word2id
        for k, v in self._txt_tag_generator():
            words = [i for i in list(seg_txt(str(k).lower())) if not i.isdigit()]
            yield word2id.id_list_by_word_list(words) , v

    def tofile(self):
        word_id2tag_id = list(self.txt_tag_generator())
        path = DATA_DIR
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
        self.tag2id = WordId().fromfile(join(DATA_DIR, 'tag2id'))
        self.word2id = WordId().fromfile(join(DATA_DIR, 'word2id'))
        self.db = DB_Kyoto('test.kch')

        for word_id_list, tag_id_list in word_id2tag_id:
            for tag_id in tag_id_list:
                topic_id_title_count[tag_id] += 1
                for word_id in word_id_list:
                    word_topic_count[word_id][tag_id] += 1

    def rank(self):
        print 'Ranking'
        topic_id_title_count = self.topic_id_title_count
        word_topic_count = self.word_topic_count


        #word_topic_bayes = {}
        for word, topic_count in word_topic_count.iteritems():
            word_topic_freq = {}
            word_doc_count = WORD_DOC_COUNT.get(word)
            x = 1/float(word_doc_count)
            for topic_id, count in topic_count.iteritems():

                word_topic_id = self.word2id.get_id_by_tag(self.tag2id.get_word_by_id(topic_id))

                topic2title = topic_id_title_count[topic_id]
                if topic2title < 10:
                    continue
                if word_topic_id != topic_id:
                    word_topic_freq[topic_id] = (count+1)/float(topic2title+word_doc_count) - x

                else:
                    word_topic_freq[topic_id] = 1

            count = sum(word_topic_freq.itervalues())
            self.db.set((word, [(k, (v+x)/(count+x*len(topic_count))) for k, v in word_topic_freq.iteritems()]))
            #wb = word_topic_bayes[word] = []
            #for k, v in word_topic_freq.iteritems():
            #    wb.append((k, v/count))

#return word_topic_bayes

def main():
    #tagword = TagWord(join(current_path, 'train_data/'))
    #tagword.tofile()
    #WORD_ID2TAG_ID = fromfile(join(DATA_DIR, 'word_id2tag_id'))
    bayes_rank = BayesRank(WORD_ID2TAG_ID)
    
    #bayes_rank.rank()
    #tofile(join(DATA_DIR, 'bayes_rank') , bayes_rank.rank())

if __name__ == '__main__':
    #TAG2ID = WordId().fromfile(join(DATA_DIR, 'tag2id'))
    #print   TAG2ID._dict.keys()
    main()
else:
    #BAYES_RANK = fromfile(join(DATA_DIR, 'bayes_rank'))
    TAG2ID = WordId().fromfile(join(DATA_DIR, 'tag2id'))
    WORD2ID = WordId().fromfile(join(DATA_DIR, 'word2id'))
