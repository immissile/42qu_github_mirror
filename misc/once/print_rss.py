#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import _env
from zkit.google.findrss import feeds, get_rss_link_title_by_rss
from model.zsite_link import ZsiteLink
from model.zsite import Zsite, ZSITE_STATE_VERIFY

def get_uri():
    ids = Zsite.raw_sql('select id from zpage.zsite where state >= %s', ZSITE_STATE_VERIFY ).fetchall()
    links = []
    for id in ids:
        link = ZsiteLink.raw_sql('select link from zpage.zsite_link where zsite_id = %s and cid = 0', *id).fetchone()
        if link:
            links.append(link[0])
    return links

import re
DOUBAN = re.compile('http://www.douban.com/people/(\w+)')
DOUBAN_RSS = ['http://www.douban.com/feed/people/%s/notes', 'http://www.douban.com/feed/people/%s/reviews']

def get_rss(links):
    for link in links:
        if link:
            a = DOUBAN.match(link)
            if a:
                douban = a.group(1)
                yield [i % douban for i in DOUBAN_RSS]
            else:
                try:
                    rss = feeds(link)
                except:
                    continue
                if rss:
                    yield rss


def print_rss():
    links = []
    m = open('x')
    for line in m:
        links.append(line.strip())

    with open('x.xml', 'w') as output:
        output.write("""<?xml version="1.0" encoding="UTF-8"?>
<opml version="1.0">
<head>
<title>Google 阅读器中 peng 的订阅</title>
</head>
<body>
""")
        for i in get_rss(links):
            for j in i:
                if j:
                    txt = get_rss_link_title_by_rss(j)[-1]
                    output.write("""<outline text="%s"
title="%s"
type="rss" xmlUrl="%s"
htmlUrl="%s"/>
""" % (txt, txt, j, j))


        output.write("""</body></opml>""")

def print_uri():
    links = get_uri()
    with open('x', 'w') as f:
        for i in links:
            f.write('%s\n' % i)

if __name__ == '__main__':
    print_uri()
    #print_rss()
