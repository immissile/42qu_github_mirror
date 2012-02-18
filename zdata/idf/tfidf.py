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
                    if j in txt:
                        has_tag = True
                        break
            elif i in txt:
                has_tag = True
                break

        if has_tag:
            result.append((tag_id, rank))

    return result



if __name__ == '__main__':
    txt = """
首先要问下自己的内心。
其实这三个选择差别都比较大。
公务员其实也分两种，国家和地方。如果你现在就想养老，或者说有更多的属于自己的时间，推荐你去地方的；如果说你想见见世面，开开眼界，去国家的。当然了，不同的部门，对你的影响的差别也很大，饭碗虽好，但第三遍劝你，入该行须谨慎。
研究生，我个人理解也有两种以上不同的可能。1.不是本科所学，学自己所爱；2.本科所学，纯粹是为了提高自己的竞争力。这个我觉得比较好区分，而且还是那句老话，自己的选择。
我最不想谈的就是记者，因为记者是个很诡异的工作，抛去战地记者等高危记者之外，累一点的跑热线，闲一点的当个跑口记者也优哉游哉，还有一群为了能跑调查性报道而挤破脑袋的人。关于记者，奉劝一句，除非你是真的很爱这个行业，不然如果有别的机会，可以先考虑其他的。
"""
    for k, v in tf_idf_seg_txt(txt)[:10]:
        print k, v

    print '>'*20

    txt = '中国李开复是一个好地方 关于记者，奉劝一句，除非你是真的很爱这个行业，不然如果有别的机会，可以先考虑其他的。'
    for k, v in tf_idf_seg_txt(txt)[:10]:
        print k, v

    print '>'*20

    txt = '''
可口可乐从来就不认为消费者会满足于他们所提供的那几种类型的饮料。所以，从这个夏天开始，在加利福尼亚、乔治亚和犹他州的一些快餐连锁店，可口可乐将尝试使用一种自助式的饮料配方机，用户可以选择30多种配料，调制超过100种的可口可乐饮料。
一线BI机器人部队
可口可乐计划在美国全国范围内使用这种自选饮料配方机，特别是在成千上万的麦当劳、汉堡王等快餐店之中。尽管这种机器所使用的客户选择理念达到了新的高度，但更有趣的是这个配方机所使用的技术。这些自选配方机将成为可口可乐在商业智能方面的一线机器人部队，它们会将庞大的消费数据返回给公司在亚特兰大的总部，用于其改进产品。
自选配方机可以让可口可乐在测试其新的配方或者新的品牌时更加轻松。每台这种机器都可以包含30种配料，提供100多种不同的饮料组合。这些配料各自有使用射频识别(RFID)技术的芯片，而配方机装有RFID读卡器。配方机收集客户喜欢喝什么，以及每种配料比例的数据，然后每天晚上将这些信息通过一个私有的Verizon无线网络传给可口可乐在亚特兰大的SAP数据仓库系统。公司将分析这些数据，编写报告介绍新饮料配方在市场上的表现，还会分析哪些地方的人更钟爱哪些口味，进而帮助快餐店决定提供哪种配方。
'''


    for k, v in tag_id_list_rank_by_txt(txt)[:10]:
        print k, v,
        for i in ID2NAME[k]:
            print i,
        print ""
