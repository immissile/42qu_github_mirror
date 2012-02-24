#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from config import GREADER_USERNAME, GREADER_PASSWORD
from zkit.google.greader import Reader
from urllib import quote
from zkit.pprint import pprint

TEMPLATE_UCD_CHINA_RSS = 'http://ucdchina.com/rss/category?id=%s'



def main():
    greader = Reader(GREADER_USERNAME, GREADER_PASSWORD)
    for id in (1, 2, 3, 6, 8):
        feed = 'feed/%s'%quote(TEMPLATE_UCD_CHINA_RSS%id)
        print feed
        for i in greader.feed(feed):
            pprint(i)

if '__main__' == __name__:
    main()

