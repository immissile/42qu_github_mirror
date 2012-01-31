#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from idf import idf_zhihu
from mmseg import seg_txt
from yajl import loads

class ParentTagger(object):
    def __init__(self):
        from generate_lib import TAG2ID
        self.word_to_id = TAG2ID.word_to_id()
        self.word_to_id = dict([(unicode(k), v) for k, v in self.word_to_id.iteritems()])

        self.id_to_word = TAG2ID.id2word()

    def sp_txt(self, txt):
        txt = unicode(txt)
        for i in range(len(txt)-1):
            yield txt[i]+txt[i+1]

    def get_parent_tag(self, tag):
        set_list = []

        for i in self.sp_txt(tag):
            if i in self.word_to_id:
                set_list.append(i)

        out = []
        for i in  set_list:
            out.append(self.word_to_id[i])
            print self.word_to_id[i], i

        return out

    def get_parent_tag_list_by_list(tag_list):
        out = []
        for tag in tag_list:
            parent_tag_id_list = self.get_parent_tag(tag)
            out.extend(parent_tag_id_list)
        return out


if __name__ == '__main__':
    finder = ParentTagger()
    print finder.get_parent_tag(u'用户体验设计')
