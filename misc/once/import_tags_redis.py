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
from model.po_by_tag import tag_alias_new, _tag_alias_new
from zkit.fanjian import utf8_ftoj

CURRNET_PATH = path.dirname(path.abspath(__file__))
TMP_REDIS = 'tmp_import_redis'
import re
from model.autocomplete import  autocomplete_tag
from collections import defaultdict

ID2NAME = defaultdict(list)
for name, id in NAME2ID.iteritems():
    ID2NAME[id].append(name)

if __name__ == '__main__':
    name_id = {}
    for i in Zsite.where(cid=CID_TAG):
        lname = i.name.strip().lower() 
        id = i.id
        for name in ID2NAME.get(id,()):
            if name.lower() not in lname:
                print i.name, name
                tag_alias_new(id, name)               
   
        autocomplete_tag.append(i.name, id)

        for j in map(utf8_ftoj, map(str.strip, i.name.split('/'))):
            _tag_alias_new(id, j)
 
 
#        id = i.id
#        rank = ID2RANK.get(id, 0)
#        name = i.name
#        autocomplete_tag.append(name, id, rank)
#        name_id[name] = id
#
#    for name , id in name_id.iteritems():
#        redis.hset(autocomplete_tag.ID2NAME, id, '%s`%s'%(name, 0))
#        print name, rank, 'id'
