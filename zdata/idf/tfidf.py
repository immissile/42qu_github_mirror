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
“空间”趣谈

（1）被洗礼的空间认识
大学里建筑初步的教育注定了学生从这类课堂上走出之后对于眼前的世界有了不一样的期待，其中的功效之一就是让学生们“学会了看空间”。

“看空间”是个很有趣的话题，仿佛是个无需证明就可自明的话题。小孩子很小就知道东南西北，知道高下远近，知道前后关系，那也就是说，人人都有体验和感知和认识和构想空间的能力。嗯，的确如此——也的确不如此，如果我们看看皮亚杰那些有关儿童地图和空间测试的成果的话。

简言之，人是这么一种动物，睁大眼睛，没有意识或是经验提醒的话，对于眼前的事物并不会特别地关注。建筑学的基础教育则通过模型和绘图，帮助学生完成了对于眼前世界特别是人造世界的“空间注意”。一个经过了建筑教育洗礼的人和一个基本上对于建筑不大关心的人，走进一个房间里，或者一系列房间里，那个没有被洗礼的人，通常会看房子里的家具、字画、花盆、地板上的花纹。。。。满眼的细节，而那个受了建筑教程洗礼的人，则“可能开始知道去看墙面，墙面材料（是水泥？是泥灰？是玻璃？是木板？）所具有的空间限定能力，以及那些由墙体界面围合出来的所谓的‘空间’”。这个差别的确存在，特别是当建筑师们变成了建筑大师们之后，他们的话语交流，老百姓基本就听不懂看不明了，以致于汉语读者看不懂汉语的建筑杂志文章，英语读者也未必就能看懂英语的建筑文章都讲了些什么东西。

这种建筑基础教育洗礼的后果还远不止看一个房间时的这点分歧。我们常会看到的一个普遍现象，那就是凡是重要建筑项目由国家leader们选方案的话，leader们无一例外地是在看“造型”，而建筑界业内人愿意推敲的则是一定会包括所谓的“空间”。当代中国建筑师已经长了一颗接受了西方现代世界观和艺术品位的脑袋。这就让建筑师跟开发商跟领导们，在审美上，很难真正走到一起去。甚至很难让建筑师跟美术系的人走到一起去。君不见，请美术系的人来装房子，如果不把墙面做得凹凸不平、三种颜色、四种质感、七个造型，美术系的人是不甘心的，业主似乎也觉得他们没有出什么力。 
    '''


    for k, v in tag_id_list_rank_by_txt(txt)[:10]:
        print k, v,
        for i in ID2NAME[k]:
            print i,
        print ""
