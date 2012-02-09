#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from model.zsite import Zsite
from model.auto_tag import auto_complete_tag
from zweb.orm import ormiter
from model.cid import CID_TAG
from model._db import redis
from import_tags import TMP_REDIS
from model.zsite_fav import zsite_fav_count_by_zsite  

if __name__ == '__main__':
    for i in ormiter(Zsite, 'cid=%s'%CID_TAG):
        print i.id, i.name
        #tag_tag.set(i.name,i.id)
        rank = redis.hget(TMP_REDIS,i.name)
        auto_complete_tag.append(i.name, i.id,rank)

    for id,name_rank in redis.hgetall(auto_complete_tag.ID2NAME).iteritems():
        zsite = Zsite.mc_get(id) 
        if zsite:
            score =  zsite_fav_count_by_zsite(zsite)
            name = name_rank.rsplit('`',1)[0]
            redis.set(auto_complete_tag.ID2NAME,id,'name`%s'%score)
        



