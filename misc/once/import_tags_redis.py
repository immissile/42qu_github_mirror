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

CURRNET_PATH = path.dirname(path.abspath(__file__))
TMP_REDIS = 'tmp_import_redis'
import re

RE_X = re.compile('#.+?#')

if __name__ == '__main__':
    Zsite.where('cid=%s',CID_TAG).delete()

    with open(path.join(CURRNET_PATH,'tag_score.js')) as d:
        score_dict = loads(d.read())
        name_id = {}

        for name , rank in score_dict.iteritems():
            name = RE_X.sub('', name)
            print name    
            id =  tag_by_str(name).id
            autocomplete_tag.append(name, id, rank)
            name_id[name] = id
            print name, rank, "rank"

        for name , id in name_id.iteritems():
            redis.hset(autocomplete_tag.ID2NAME, id, '%s`%s'%(name, 0))
            print name, rank, "id"


