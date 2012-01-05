#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import _env
import urllib2
from zkit.htm2txt import htm2txt
from urllib2 import urlopen
from zkit.bot_txt import txt_wrap_by_all, txt_wrap_by
import os.path as path
from zkit.spider import Rolling, Fetch, NoCacheFetch, GSpider
from time import sleep
from os.path import exists
import os.path
from yajl import dumps
from hashlib import md5
import threading
from zkit.lock_file import LockFile
from writer import Writer,CURRNET_PATH
from zkit.classification.classification import GetTag  
from rss_po import RssPo

TAGGER = GetTag()

def name_builder(url):
    return os.path.join(CURRNET_PATH, "ucdchina", path.basename( url))

def parse_page(filepath):
    with open(filepath) as f:
        page = f.read()

        title = txt_wrap_by('<title>', '- UCD大社区', page)
        author = txt_wrap_by('style=" float:left; color:#999;">', '</span', page)
        author = txt_wrap_by('作者：', '|', author)
        content_wrapper = txt_wrap_by('<div id="pageContentWrap" style="font-size:13px; ">', '</div', page)

        if content_wrapper:
            content,pic_list = htm2txt(content_wrapper)
        else:
            return 
        
        content = str(content)
        tags = TAGGER.get_tag(content+title)
        out = dumps([ title, content, author, tags ])

        a = RssPo(content,2585,title, pic_list, 0, 2585,tags)
        a.htm2po_by_po()

        writer = Writer.get_instance()
        writer = writer.choose_writer('ucdchina.data')
        writer.write(out+'\n')

def save_page(page, url):
    filename = name_builder(url)
    with open(filename, 'w') as f:
        f.write(page)
    parse_page(filename)

def parse_index(page, url):
    link_wrapper_list = txt_wrap_by_all('<div id="mainWrap">', '<!--/#mainWrap', page)
    link_list = []
    for link_wrapper in link_wrapper_list:
        url = txt_wrap_by('/snap/', '"', link_wrapper)
        filename = name_builder(url)
        if not exists(filename):
            yield save_page, 'http://ucdchina.com/snap/'+url
        else:
            parse_page(filename)

def ucdchina_daily():
    word_list = ['PM', 'UCD', 'UR', 'ia-id', 'VD', 'HappyDesign']
    for typ in word_list:
        yield parse_index, 'http://ucdchina.com/%s'%str(typ)

def ucd_url_builder():
    for page in xrange(68):
        yield parse_index, 'http://ucdchina.com/PM?p=%s'%str(page)
    for page in xrange(1256):
        yield parse_index, 'http://ucdchina.com/UCD?p=%s'%str(page)
    for page in xrange(393):
        yield parse_index, 'http://ucdchina.com/UR?p=%s'%str(page)
    for page in xrange(1374):
        yield parse_index, 'http://ucdchina.com/ia-id?p=%s'%str(page)
    for page in xrange(297):
        yield parse_index, 'http://ucdchina.com/VD?%p=%s'%str(page)
    for page in xrange(1133):
        yield parse_index, 'http://ucdchina.com/HappyDesign?p=%s'%str(page)

def main():
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
            'Accept': ' text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
            'Accept-Language':'zh-cn,zh;q=0.5',
            'Accept-Charset':'gb18030,utf-8;q=0.7,*;q=0.7',
            'Content-type':'application/x-www-form-urlencoded'
    }

    fetcher = NoCacheFetch(0, headers=headers)
    spider = Rolling( fetcher, ucd_url_builder() )
    spider_runner = GSpider(spider, workers_count=10)
    spider_runner.start()

if __name__ == '__main__':
    main()
