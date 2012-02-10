#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from collections import defaultdict
from tfidf.idf import idf_zhihu
from mmseg import seg_txt
from yajl import loads
from zkit.sp_txt import sp_txt

class ParentTagger(object):
    def __init__(self):
        from train import TAG2ID 
        self.word_to_id = TAG2ID.word_to_id()
        self.word_to_id = dict([(unicode(k),v) for k,v in self.word_to_id.iteritems()])

        self.id_to_word = TAG2ID.id2word()

    def get_parent_tag(self, tag):
        set_list = []

        for i in sp_txt(tag):
            if i in self.word_to_id:
                set_list.append(i)

        return list(set(set_list))

    def get_parent_tag_list_by_list(self,tag_list):
        out = []
        for tag in tag_list:
            parent_tag_list = self.get_parent_tag(tag)
            out.extend(parent_tag_list)
        return out
    
if __name__ == '__main__':
    finder = ParentTagger()
    print ','.join(finder.get_parent_tag(u'用户体验设计'))
