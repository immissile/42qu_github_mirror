#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from config import ZDATA_PATH
from zkit.tofromfile import tofile, fromfile
from idf import tf_idf as _tf_idf
from os.path import join
from mmseg import seg_txt

IDF = fromfile(join(ZDATA_PATH, "data/idf"))

def tf_idf(word_list):
    return _tf_idf(word_list, IDF)

def tf_idf_seg_txt(txt):
    word_list = list(seg_txt(word_list))
    return tf_idf(word_list)

if __name__ == "__main__":
    txt = """
首先要问下自己的内心。
其实这三个选择差别都比较大。
公务员其实也分两种，国家和地方。如果你现在就想养老，或者说有更多的属于自己的时间，推荐你去地方的；如果说你想见见世面，开开眼界，去国家的。当然了，不同的部门，对你的影响的差别也很大，饭碗虽好，但第三遍劝你，入该行须谨慎。
研究生，我个人理解也有两种以上不同的可能。1.不是本科所学，学自己所爱；2.本科所学，纯粹是为了提高自己的竞争力。这个我觉得比较好区分，而且还是那句老话，自己的选择。
我最不想谈的就是记者，因为记者是个很诡异的工作，抛去战地记者等高危记者之外，累一点的跑热线，闲一点的当个跑口记者也优哉游哉，还有一群为了能跑调查性报道而挤破脑袋的人。关于记者，奉劝一句，除非你是真的很爱这个行业，不然如果有别的机会，可以先考虑其他的。
"""
    for k, v in tf_idf_seg_txt(txt):
        print k,v 

