#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model
from zsql.hash import by_hash, save_hash
from zkit.shorturl import t_cn, dwz_cn, curt_cc


SHORTURL_CID_SINA = 1
SHORTURL_CID_DWZ = 2
SHORTURL_CID_CURT = 3
SHORTURL_CID_XRL = 4

class Shorturl(Model):
    by_url_hash = by_hash('url')

    def save(self):
        url = self.url
        save_hash(self, 'url')
        super(Shorturl, self).save()

NOW_SHORTURL_CID = SHORTURL_CID_CURT

SHORTURL_CID2SHORT = {
    SHORTURL_CID_SINA:t_cn,
    SHORTURL_CID_DWZ:dwz_cn,
    SHORTURL_CID_CURT:curt_cc
}
SHORTURL_CID2URL = {
    SHORTURL_CID_SINA:'http://t.cn/',
    SHORTURL_CID_DWZ:'http://dwz.cn/',
    SHORTURL_CID_CURT:'http://curt.cc/',
    SHORTURL_CID_XRL:'http://xrl.us/'
}



def shorturl(url):
    ms = Shorturl.by_url_hash(url)
    if ms:
        prefix = SHORTURL_CID2URL[ms.cid]
        return prefix+ms.shorturl
    else:
        short = SHORTURL_CID2SHORT[NOW_SHORTURL_CID](url)
        s = Shorturl()
        s.url = url
        s.cid = NOW_SHORTURL_CID
        s.shorturl = short[
            len(SHORTURL_CID2URL[NOW_SHORTURL_CID]):
        ]
        s.save()
        return short


if '__main__' == __name__:
    url = 'http://baidu.com?233'
    print shorturl(url)
