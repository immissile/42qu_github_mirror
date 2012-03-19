#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
import urllib2
from urllib import urlencode 
from zkit.pic import picopen 
from json import loads
from zkit.bot_txt import txt_wrap_by_all, txt_wrap_by
import os.path as path
from xml.sax.saxutils import unescape
from zkit.htm2txt import htm2txt
from zkit.spider import Rolling, Fetch, NoCacheFetch, GSpider
from time import sleep
from os.path import exists
import os.path
from zkit.earth import PID2NAME
import re
from yajl import dumps,loads
import threading
from writer import Writer,CURRNET_PATH,Spider, url_is_fetched,Spider


#out_f = open("dongxi.data",'w')

class Dongxi(object):
    def __init__(self):
        pass

    def daily_dongxi(self):
        yield self.parse_index,'http://dongxi.net/index/original?type=channel&slug=all&cate=havetrans'

    def dongxi_crawler(self):
        for i in xrange(1,695):
            yield self.parse_index,'http://dongxi.net/index/original?type=channel&slug=all&cate=havetrans&page=%s'%str(i)

    def parse_index(self,page,url):
        link_wrap_list = txt_wrap_by_all('已翻译','<span',page)
        link_list = []
        for link_wrap in link_wrap_list:
            url = txt_wrap_by('href="','"',link_wrap)
            if url and not url_is_fetched(url):
                yield self.parse_page,'http://dongxi.net/%s'%url

    def parse_page(self,page,url):
        print "Dongxi...%s"%url
        title = txt_wrap_by('<div class="content_title clearfix">','</h1>',page).strip().split('>')[-1].strip()
        author = txt_wrap_by('<a class="link_text_blue" href="','</a>',page).strip().split('>')[-1].strip()

        tags = map(lambda x:x.split('>')[-1],txt_wrap_by_all("<a  class='link_text_blue'",'</a>',page))
        rating_num = txt_wrap_by('onclick="favorate(',')',page)
        
        content = txt_wrap_by('id="full_text">','</div',page)

        yield self.parse_rat,'http://dongxi.net/content/widget/page_id/%s'%rating_num,title,author,tags, url,content

    def parse_rat(self,page,url,title,author,tags, po_url, content):
        rating = 0
        try:
            dic = loads(page)
            rating = dic['fav_count']
        except:
            pass

        content,pic_list = htm2txt(content)
        content = str(content)
        pic_list = ['http://dongxi.net'+i for i in pic_list]

        out = dumps([title,tags,content ,author ,rating, po_url,None ])
        #Spider.insert(title, tags, content, author, rating ,url, None, pic_list)
        print out
        #print >>out_f,out 
        raw_input()

        #writer = Writer.get_instance()
        #writer = writer.choose_writer('dongxi.data')
        #writer.write(out+'\n')

def main():
    headers = {
    }

    dongxi = Dongxi()
    fetcher = NoCacheFetch(0,headers=headers)
    spider = Rolling(fetcher,dongxi.daily_dongxi())
    spider_runner = GSpider(spider, workers_count=3)
    spider_runner.start()

if __name__ == '__main__':
    main()
