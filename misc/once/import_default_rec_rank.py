#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from model.zsite import Zsite
from model.auto_tag import auto_complete_tag
from zweb.orm import ormiter
from model.cid import CID_TAG
from model._db import redis
from model.zsite_fav import zsite_fav_count_by_zsite
from os import path
from yajl import loads
from model.po_by_tag import  tag_by_name
from zkit.bot_txt import txt_map
from model.zsite import zsite_new, ZSITE_STATE_ACTIVE


CURRNET_PATH = path.dirname(path.abspath(__file__))
TMP_REDIS = 'tmp_import_redis'
import re

RE_X = re.compile('#.+?#')

if __name__ == '__main__':
    #Zsite.where('cid=%s', CID_TAG).delete()
    #kv = redis.hgetall(auto_complete_tag.ID2NAME)
    #for id, name in kv.iteritems():
    #    name = name.split('`')[0]
    #    zsite_new(name, CID_TAG, ZSITE_STATE_ACTIVE, id)
    #    print id, name

     
    with open(path.join(CURRNET_PATH, 'tag_score.js')) as d:
        score_dict = loads(d.read())

        nr_dict = dict(
            (i.name, i.id) for i in
            Zsite.where('cid=%s', CID_TAG)
        )
        for pos, (name , rank) in enumerate(sorted(score_dict.iteritems(), key=lambda x:-x[1])[:1024]):
            name = RE_X.sub('', name)
            print pos, name, rank, nr_dict[str(name)]

