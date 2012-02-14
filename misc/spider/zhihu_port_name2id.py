#!/usr/bin/env python
# -*- coding: utf-8 -*-

from zhihu_topic_url2id import ID2MY
from zhihu_topic_data_20120211 import ZHIHU_TOPIC
from model.zsite import Zsite
from itertools import chain

def main():
    for zhihu_topic in ZHIHU_TOPIC:
        id = zhihu_topic[0]
        name = zhihu_topic[1]
        alias_list = zhihu_topic[5]
        
        if id in ID2MY:
            tag = Zsite.mc_get(ID2MY[id])
            if tag:
                ori_tag = tag.name
                for i in chain(map(str.strip, ori_tag.split("/")),alias_list):
                    #result[i]=ID2MY[id]
                    print '"%s":%s,'%(i,str(ID2MY[id]))
                 #redis - >baidu tag_id



if __name__ == '__main__':
    main()
