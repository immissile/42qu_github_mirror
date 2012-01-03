#!/usr/bin/env python # -*- coding: utf-8 -*-

import _env
import urllib2
from urllib2 import urlopen
from zkit.bot_txt import txt_wrap_by_all, txt_wrap_by
import os.path as path
from zkit.spider import Rolling, Fetch, NoCacheFetch, GCrawler
from time import sleep
from os.path import exists
import os.path
from yajl import dumps
from hashlib import md5
import threading

#FILE_LOCK = threading.RLock()
CURRNET_PATH = path.dirname(path.abspath(__file__))
#WRITER = open('yeeyan.data','w')

def name_builder(url):
    return os.path.join(CURRNET_PATH,"yeeyan", md5(url).hexdigest())

def parse_page(filepath):
    with open(filepath) as f:
        page = f.read()

        title = txt_wrap_by('<title>译言网 | ', '</ti', page)
        tags_wrapper = txt_wrap_by('class="tags bdr">', '</div', page)
        tags_wrapper = tags_wrapper.replace('<b>Tags:</b>','')
        tags = txt_wrap_by_all("'>", '</a', tags_wrapper)
        author = txt_wrap_by('<h2 id="user_info"', '/a', page)
        author = txt_wrap_by('">','<',author)
        rating = txt_wrap_by('已有<span class="number">', '</span', page)

        reply_wrapper_list = txt_wrap_by_all('class="comment_content">', '</ul', page)
        reply_list = []
        for reply_wrapper in reply_wrapper_list:
            reply_list.append(txt_wrap_by('<p>', '</p', reply_wrapper))

        out = dumps([ title, tags, author, rating , reply_list])
        print title,tags,author,rating,reply_list

def save_page(page,url):
    with open(name_builder(url),'w') as f:
        f.write(page)

def parse_index(page, url):
    link_wrapper_list = txt_wrap_by_all('<h5 clas', '</h5', page)
    link_list = []
    for link_wrapper in link_wrapper_list:
        url = txt_wrap_by('href="', '"', link_wrapper)
        if not exists(name_builder(url)):
            yield save_page, url

def yeeyan_url_builder():
    for page in xrange(1, 5001):
        yield parse_index, 'http://article.yeeyan.org/list_a?page=%s'%str(page)

def main():
    headers = {
        'Cookie':'bid=i9gsK/lU40A',
    }

    fetcher = NoCacheFetch(0, headers=headers)
    spider = Rolling( fetcher, yeeyan_url_builder() )
    spider_runner = GCrawler(spider, workers_count=1)
    spider_runner.start()

if __name__ == '__main__':
    main()
