#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kv import Kv

motto = Kv('motto')

motto_get = motto.get
motto_set = motto.set

if __name__ == '__main__':
    motto_set(47036, 'this is the motto of 新闻媒体')
