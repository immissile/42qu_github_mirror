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
    ids = Zsite.raw_sql('select id from zpage.zsite where state >= %s',ZSITE_STATE_VERIFY ).fetchall()
    links = []
    for id in ids:
        links.append(ZsiteLink.raw_sql('select link from zpage.zsite_link where zsite_id = %s and cid = 0',*id).fetchone())
    for link in links:
        if link:
            try:
                rss = feeds(*link)
            except:
                continue
            if rss:
                yield rss



if __name__ == '__main__':
    with open("x.xml","w") as output:
        output.write( """<?xml version="1.0" encoding="UTF-8"?>
<opml version="1.0">
<head>
<title>Google 阅读器中 peng 的订阅</title>
</head>
<body>
        """)
        for i in get_uri():
            if i[0]:
                txt = get_rss_link_title_by_rss(i[0])[-1]
                output.write( """<outline text="%s"
                                  title="%s" 
                type="rss" xmlUrl="%s"
                htmlUrl="%s"/>
                """%(txt,txt,i[0],i[0]))


        output.write( """
    </body>
    </opml>
        """)



