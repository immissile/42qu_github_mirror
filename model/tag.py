#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kv import Kv

Tag = Kv('tag')

def tag_new(tag):
    tag = tag.strip().replace(' ', '_')
    return Tag.mc_id_by_value_new(tag)

tag_get = Tag.get
tag_set = Tag.set

if __name__ == '__main__':
    pass
