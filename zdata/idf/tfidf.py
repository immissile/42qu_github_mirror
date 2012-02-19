#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from config import ZDATA_PATH
from zkit.tofromfile import tofile, fromfile
from idf import tf_idf as _tf_idf
from os.path import join
from mmseg import seg_txt

IDF = fromfile(join(ZDATA_PATH, 'data/idf'))

def tf_idf(word_list):
    return _tf_idf(word_list, IDF)

def tf_idf_seg_txt(txt):
    txt = txt.replace('。', ' ').replace('，', ' ')
    word_list = list(seg_txt(txt))
    return tf_idf(word_list)


from kyotocabinet import DB
from collections import defaultdict
from array import array
from zkit.zitertools import chunkiter
from operator import itemgetter
from zdata.tag.name2id import NAME2ID
from zkit.txt_cleanup import sp_txt

ID2NAME = defaultdict(list)
for name, id in NAME2ID.iteritems():
    ID2NAME[id].append(name)

db_tag_bayes = DB()
db_tag_bayes.open(join(ZDATA_PATH,"data/bayes.kch"), DB.OREADER)


def tag_id_list_rank_by_txt(txt):
    txt = txt.lower()
    tag_id_list_rank = defaultdict(int)
    for word, rank in tf_idf_seg_txt(txt):
        #print word
        ars = db_tag_bayes.get(word)
        if ars:
            ar = array('I')
            ar.fromstring(ars)
            #print len(ar)
            #print db_tag_bayes[word]
            #print word, ar
            for tag_id, bayes in chunkiter(ar,2):
                tag_id_list_rank[tag_id]+=(bayes*rank)

    result = []

    for tag_id, rank in sorted(
        tag_id_list_rank.iteritems(),
        key=itemgetter(1),
        reverse=True
    ):
        has_tag = False

        if tag_id not in ID2NAME:
            continue

        for i in ID2NAME[tag_id]:
            if has_tag:
                break

            tag_list = list(sp_txt(i))

            if tag_list:
                for j in tag_list:
                    #print j, str(j) in txt
                    if str(j) in txt:
                        has_tag = True
                        break
            elif i in txt:
                has_tag = True
                break

        if has_tag:
            result.append((tag_id, rank))

    return result



if __name__ == '__main__':
    from model.feed_import import FeedImport
    from zkit.orm import ormiter

    for i in ormiter(FeedImport):
        print i.title

#    from glob import glob
#    filelist = glob("/home/guohaochuan/42qu-data/tfidf/test/articles/*.txt")
#    for i in filelist:
#        with open(i) as f:
#            txt = f.read()
#            txt += "\n\n"+i.rsplit("/")[-1][:-4]
#            print txt
#            for k, v in tag_id_list_rank_by_txt(txt)[:7]:
#                print k, v,
#                for i in ID2NAME[k]:
#                    print i,
#                print ""
#            print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

