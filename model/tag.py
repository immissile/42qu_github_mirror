#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kv import Kv

Tag = Kv('tag')

def tag_new(tag):
    tag = tag.strip()
    return Tag.mc_id_by_value_new(tag)

def tag_get(id):
    if id:
        return Tag.get(id)
    return ''

if __name__ == '__main__':
    print tag_new('test1234test134')
