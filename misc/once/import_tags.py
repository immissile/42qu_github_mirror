#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from model.po_by_tag import  tag_by_name
from yajl import loads
from os import path
from model._db import redis

CURRNET_PATH = path.dirname(path.abspath(__file__))
TMP_REDIS = 'tmp_import_redis'

def main():
    with open(path.join(CURRNET_PATH, 'tags.data')) as f:
        with open(path.join(CURRNET_PATH,'tag_score.js')) as d:
            score_dict = loads(d.read())
            data = loads(f.read())

            for k,v in data.iteritems():
                name = '/'.join(v)
                id =  tag_by_name(name).id
                redis.hset(TMP_REDIS,name,score_dict[k])
                

if __name__ == '__main__':
    main()
