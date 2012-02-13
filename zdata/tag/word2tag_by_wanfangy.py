#coding:utf-8
import _env
from name2id import NAME2ID
from mmseg import seg_txt
from glob import glob
from name2id import NAME2ID
from json import loads
from zkit.pprint import pprint
from math import log
from collections import defaultdict
from zkit import tofromfile
from word2tag import train

NAME2ID_SET = set(NAME2ID)
WORD2TAG_COUNT = {}

def wangfang_parser(fn):
    with open(fn) as infile:
        for line in infile:
            s = loads(line.strip())
            if not s[2]:
                continue
            txt = "\n".join(filter(bool,s[:2])).strip()
            if not txt:
                continue
            tag_list = set(str(i).replace('·', '.').lower() for i in s[2])
            exist_tag = tag_list&NAME2ID_SET
            if exist_tag:
                exist_id_list = list(NAME2ID[i] for i in exist_tag)
                yield exist_id_list , txt


for fn in glob("/mnt/zdata/train/df/wanfang/*"):
    if "." in fn:
        continue
    train(fn, wangfang_parser)


#            exist_tag = tag_list&NAME2ID_SET
#            if exist_tag:
#                word_list = list(seg_txt(str(txt)))
#                word2count = defaultdict(int)
#                for i in word_list:
#                    word2count[i] += 1
#                for i in exist_tag:
#                    id = NAME2ID[i]
#                    for k, v in word2count.iteritems():
#                        if k not in WORD2TAG_COUNT:
#                            WORD2TAG_COUNT[k] = {}
#                        t = WORD2TAG_COUNT[k]
#                        if id not in t:
#                            t[id] = 0
#                        t[id] += (1+log(float(v)))
#
#tofromfile.tofile("wanfang_word_tag_id_rank.tag", WORD2TAG_COUNT)



