#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kv import Kv

Tag = Kv('tag')

if __name__ == '__main__':
    for k, v in Tag.iteritems():
        print k, v

