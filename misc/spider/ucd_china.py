#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from config import GREADER_USERNAME, GREADER_PASSWORD
from zkit.google.greader import Reader
from urllib import quote
from json import dumps

TEMPLATE_UCD_CHINA_RSS = 'http://ucdchina.com/rss/category?id=%s'



def main():
    greader = Reader(GREADER_USERNAME, GREADER_PASSWORD)
    count = 0
    with open("ucd_china.js","w") as ucd_china:
        for id in (1, 2, 3, 6, 8):
            feed = 'feed/%s'%quote(TEMPLATE_UCD_CHINA_RSS%id)
            print feed
            for i in greader.feed(feed):
                ucd_china.write(dumps(i)+"\n")
                count += 1 
                print count

if '__main__' == __name__:
    main()

