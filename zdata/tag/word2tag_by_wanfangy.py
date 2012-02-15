#coding:utf-8
import _env
from name2id import NAME2ID
from glob import glob
from json import loads
from word2tag import train
from name_tidy import name_tidy

NAME2ID_SET = set(NAME2ID)

def wangfang_parser(fn):
    with open(fn) as infile:
        for line in infile:
            s = loads(line.strip())
            if not s[2]:
                continue
            txt = "\n".join(filter(bool,s[:2])).strip()
            if not txt:
                continue
            tag_list = set(name_tidy(i) for i in s[2])
            exist_tag = tag_list&NAME2ID_SET
            if exist_tag:
                exist_id_list = list(NAME2ID[i] for i in exist_tag)
                yield exist_id_list , txt


for fn in glob("/mnt/zdata/train/df/wanfang/*"):
    if "." in fn:
        continue
    print fn
    train(fn, wangfang_parser)


#            exist_tag = tag_list&NAME2ID_SET
#            if exist_tag:
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



