#coding:utf-8
import _env
from name2id import NAME2ID
from mmseg import seg_txt
from glob import glob
from name2id import NAME2ID 
from json import loads
from zkit.pprint import pprint

WORD2TAG_COUNT = {}

for i in glob("/mnt/zdata/train/df/wanfang/*"):
    if "." in i:
        continue
    with open(i) as infile:
        for line in infile:
            s = loads(line.strip())
            pprint(s)



