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
from model.zsite import zsite_new, ZSITE_STATE_ACTIVE
from model.zsite_list import zsite_list_new, ZsiteList
import re

CURRNET_PATH = path.dirname(path.abspath(__file__))
TMP_REDIS = 'tmp_import_redis'

RE_X = re.compile('#.+?#')

if __name__ == '__main__':
    #Zsite.where('cid=%s', CID_TAG).delete()
    #kv = redis.hgetall(autocomplete_tag.ID2NAME)
    #for id, name in kv.iteritems():
    #    name = name.split('`')[0]
    #    zsite_new(name, CID_TAG, ZSITE_STATE_ACTIVE, id)
    #    print id, name
    #with open(path.join(CURRNET_PATH, 'tag_score.js')) as d:
    #    score_dict = loads(d.read())

    #    nr_dict = dict(
    #        (i.name, i.id) for i in
    #        Zsite.where('cid=%s', CID_TAG)
    #    )
    #    for pos, (name , rank) in enumerate(sorted(score_dict.iteritems(), key=lambda x:-x[1])):
    #        name = RE_X.sub('', name)
    #        zsite_list_new(
    #            nr_dict[str(name)],
    #            0,
    #            CID_TAG,
    #            rank  
    #        )
    #        print pos, name 

    #print Zsite.where(cid=CID_TAG).count()
    #print ZsiteList.where(cid=CID_TAG,owner_id=0).count()

