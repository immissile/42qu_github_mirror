#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from model.po_by_tag import  tag_by_name
from yajl import loads
from os import path

CURRNET_PATH = path.dirname(path.abspath(__file__))

def main():
    with open(path.join(CURRNET_PATH, 'tags.data')) as f:
        data = loads(f.read())
        for k,v in data.iteritems():
            print tag_by_name('/'.join(v)).id, k

if __name__ == '__main__':
    main()
