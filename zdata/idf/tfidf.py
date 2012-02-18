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
    ID2NAME[name].append(id)

db_tag_bayes = DB()
db_tag_bayes.open(join(ZDATA_PATH,"data/bayes.kch"), DB.OREADER)


def tag_id_list_rank_by_txt(txt):
    txt = txt.lower()
    tag_id_list_rank = defaultdict(int)
    for word, rank in tf_idf_seg_txt(txt):
        if word in db_tag_bayes:
            ar = array('I')
            ar.fromstring(db_tag_bayes[word])
            #print db_tag_bayes[word]
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

    txt = '''在实现向量空间模型或其他检索模型时，我们通常使用倒排索引（inverted index）来避免在每篇文档中使用冗长的顺序查找来查找查询词。因此，在用户提交查询之前，我们首先构造倒排索引表。从图2-3中我们可以看到倒排索引表的结构。n个词项中的每一项都被存储在称为索引的结构中。对于每一个词项，指向的逻辑链接表被称作倒排表（posting list）。倒排表记录每篇包含该词项的文档。在图2-3中，倒排表中记录了文档标识符和词频等信息。（实际上，人们往往使用比链接表更有效的结构，但从概念上讲都是为了同一目的。）图中的倒排表表明词项t1在文档1中出现了一次，在文档10中出现了两次。对于一个任意的词项t1的条目，表明该词项在文档j中出现了tf次。倒排索引的的具体构造细节和用法将在第5章中介绍，不过知道倒排索引通常在各种检索模型中用来提高运行效率是非常有用的。
 
图2-3　倒排索引
在20世纪60年代后期的文献[Salton和Lesk，1968]中就有关于向量空间模型的早期研究。该模型在20世纪70年代中期使用非常普遍[Salton等人，1975]，并且现在仍然是计算查询和文档相似度最广泛使用的方法之一[TREC，2003]。这种方法非常重要，因为检索系统可以据此决定最终将哪些文档展示给用户。通常用户只需要最前面的n篇文档，并且这些文档按相似度进行排序。

接下来，科研人员研究了提升基本的tf-idf权重的词项权重计算方式 [Salton和Buckley，1988]。人们研究了许多不同的方法，并且认为用下面的公式计算文档i中词项j的权重效果出色：

 

这样计算权重的出发点是：在已知的查询和文档中，词频很高的匹配词项淹没了其他匹配词项的效果。为了避免这种现象，科研人员提出使用lg(tf) + 1来缩小词频的范围。基于该思想的修订版本是在查询和文档中的词项使用不同的权重。

一种被称作lnc.ltc的词项权重计算模式非常有效。文档中使用1+lg(tf)×idf计算权重，查询中使用1+lg(tf)计算权重。标签lnc.ltc是如下形式：qqq.ddd，其中qqq指查询权重，ddd指文档权重。这三个字母：qqq或ddd是xyz的形式。

第一个字母x可以是n、l或a。n表示原始词频或指tf。l表示通过取对数来降低权重，所以可以使用1+lg(tf)。a表示加强权重，所以权重为 。

第二个字母y表示是否使用idf。n表示不使用idf，t表示使用idf。

第三个字母z表示是否使用文档长度归一化。通过归一化文档长度，我们试着减小检索中文档长度的影响（见公式2-1）。在文献[Singhal, 1997]中，n表示不使用归一化，c表示使用标准的余弦归一化，u表示使用临界点长度（pivoted length）归一化。

【责任编辑：云霞 TEL：（010）'''


    for k, v in tag_id_list_rank_by_txt(txt)[:10]:
        print k, v,
        for i in ID2NAME[k]:
            print i,
        print ""
