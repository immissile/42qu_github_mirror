#!/usr/bin/env python
# -*- coding: utf-8 -*-

from zhihu_topic_url2id import ID2MY
from zhihu_topic_data_20120211 import ZHIHU_TOPIC
from model.zsite import Zsite
from itertools import chain
from model.cid import CID_TAG
from zkit.pprint import pprint

MY2ID = dict((k,v) for v,k in ID2MY.iteritems())
def main():
    id2alias = {}
    for zhihu_topic in ZHIHU_TOPIC:
        id = zhihu_topic[0]
        alias_list = zhihu_topic[5]
        id2alias[int(id)] = alias_list


    name2id = {}

    for i in Zsite.where(cid=CID_TAG):
        tag_list = map(str.strip, i.name.split("/"))
        zhihu_id = MY2ID[i.id]
        alias_list = id2alias.get(zhihu_id,())

        tag_list.extend(alias_list)
       
        for name in tag_list:
            name2id[name.lower()] = i.id

    print """
#coding:utf-8

NAME2ID = """
    pprint(name2id)

if __name__ == '__main__':
    main()

