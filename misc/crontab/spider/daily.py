#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from zkit.spider import Rolling, NoCacheFetch, GSpider
from ucdchina import UCDchina
from hashlib import md5

def pagelister():
    #for url in  Dongxi().daily_dongxi():
    #    yield url
    for url in  UCDchina().ucdchina_daily():
        yield url
    #for url in Yeeyan().yeeyan_daily():
    #    yield url

def main():
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
            'Accept': ' text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
            'Accept-Language':'zh-cn,zh;q=0.5',
            'Accept-Charset':'gb18030,utf-8;q=0.7,*;q=0.7',
            'Content-type':'application/x-www-form-urlencoded'
    }
    fetcher = NoCacheFetch(0, headers=headers)
    spider = Rolling( fetcher, pagelister() )
    spider_runner = GSpider(spider, workers_count=10)
    spider_runner.start()

if __name__ == '__main__':
    main()
