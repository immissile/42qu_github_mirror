#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from model.zsite import Zsite
from model.autocomplete import autocomplete_tag
from zweb.orm import ormiter
from model.cid import CID_TAG
from model._db import redis
from model.zsite_fav import zsite_fav_count_by_zsite
from os import path
from yajl import loads
from model.po_by_tag import  tag_by_str
from zkit.bot_txt import txt_map
from misc.spider.zhihu_topic_id_rank import ID2RANK
from zdata.tag.name2id import NAME2ID

CURRNET_PATH = path.dirname(path.abspath(__file__))
TMP_REDIS = 'tmp_import_redis'
import re
from collections import defaultdict

ID2NAME = defaultdict(list)
for name, id in NAME2ID.iteritems():
    ID2NAME[id].append(name)

if __name__ == '__main__':
    name_id = {}
    for i in Zsite.where(cid=CID_TAG):
        lname = i.name.lower() 
        for name in ID2NAME.get(i.id,()):
            name = name.lower()
            if name not in lname:
                print i.name, name 
    
 
#        id = i.id
#        rank = ID2RANK.get(id, 0)
#        name = i.name
#        autocomplete_tag.append(name, id, rank)
#        name_id[name] = id
#
#    for name , id in name_id.iteritems():
#        redis.hset(autocomplete_tag.ID2NAME, id, '%s`%s'%(name, 0))
#        print name, rank, 'id'
