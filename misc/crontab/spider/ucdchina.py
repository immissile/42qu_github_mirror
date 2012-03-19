#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import _env
import urllib2
from zkit.htm2txt import htm2txt
from zkit.bot_txt import txt_wrap_by
import os.path as path
#from zkit.spider import Rolling, Fetch, NoCacheFetch, GSpider
from time import sleep
from os.path import exists
import os.path
from yajl import dumps
from hashlib import md5
import threading
from zkit.lock_file import LockFile
from writer import Writer,CURRNET_PATH
#from zkit.classification.classification import GetTag  
#from rss_po import RssPo

#TAGGER = GetTag()
#SETTINGS HERE
UCDCHINA_ZSITE_ID = 2585
UCD_USER_ID = 2585

class UCDchina(object):
    def __init__(self):
        pass

    #def name_builder(self,url):
    #    return os.path.join(CURRNET_PATH, "ucdchina", path.basename(url))

    def parse_page(self,filepath):
        with open(filepath) as f:
            page = f.read()

            title = txt_wrap_by('<title>', '- UCD大社区', page)
            author = txt_wrap_by('style=" float:left; color:#999;">', '</span', page)
            author = txt_wrap_by('作者：', '|', author)
            content_wrapper = txt_wrap_by('<div id="pageContentWrap" style="font-size:13px; ">', '</div', page)
            url =txt_wrap_by('阅读和发布评论：<a href="','"',page)
            blog_url = txt_wrap_by('>推荐您进入文章源地址阅读和发布评论：<a href="','"',page)

            if content_wrapper:
                content,pic_list = htm2txt(content_wrapper.decode('utf-8','ignore' ))
            else:
                return 
            
            content = str(content)
            tags = TAGGER.get_tag(content+title)
            #tags = TAGGER.get_tag(content+title)
            #out = dumps([title,url,tags])
            #print out
            out = dumps([ title, content, author, tags ])
            #out = dumps([ title, content, author, blog_url ])
            print out

            #a = RssPo(content,UCD_USER_ID,title, pic_list, 0, UCDCHINA_ZSITE_ID,tags)
            #a.htm2po_by_po() 

           #writer = Writer.get_instance()
           #writer = writer.choose_writer('ucdchina.data')
           #writer.write(out+'\n')

    #def save_page(self,page, url):
    #    filename = self.name_builder(url)
    #    with open(filename, 'w') as f:
    #        f.write(page)
    #    self.parse_page(filename)

    #def parse_index(self,page, url):
    #    link_wrapper_list = txt_wrap_by('<div id="mainWrap">', '<!--/#mainWrap', page)
    #    link_list = []

    #    url_list = txt_wrap_by_all('/snap/', '"', link_wrapper_list)
    #    for url in url_list:
    #        filename = self.name_builder(url)
    #        if 'img src' in url:
    #            continue
    #        if not exists(filename):
    #            yield self.save_page, 'http://ucdchina.com/snap/'+url
    #        else:
    #            print "using cache",url
    #            self.parse_page(filename)

    #def ucdchina_daily(self):
    #    word_list = ['PM', 'UCD', 'UR', 'IA-ID', 'VD', 'HappyDesign']
    #    for typ in word_list:
    #        yield self.parse_index, 'http://ucdchina.com/%s'%str(typ)

    #def ucd_url_builder(self):
    #    for page in xrange(68):
    #        yield self.parse_index, 'http://ucdchina.com/PM?p=%s'%str(page)
    #    for page in xrange(62):
    #        yield self.parse_index, 'http://ucdchina.com/UCD?p=%s'%str(page)
    #    for page in xrange(19):
    #        yield self.parse_index, 'http://ucdchina.com/UR?p=%s'%str(page)
    #    for page in xrange(68):
    #        yield self.parse_index, 'http://ucdchina.com/IA-ID?p=%s'%str(page)
    #    for page in xrange(14):
    #        yield self.parse_index, 'http://ucdchina.com/VD?p=%s'%str(page)
    #    for page in xrange(56):
    #        yield self.parse_index, 'http://ucdchina.com/HappyDesign?p=%s'%str(page)

def main():
    #headers = {
    #        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
    #        'Accept': ' text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
    #        'Accept-Language':'zh-cn,zh;q=0.5',
    #        'Accept-Charset':'gb18030,utf-8;q=0.7,*;q=0.7',
    #        'Content-type':'application/x-www-form-urlencoded'
    #}

    ucd_china = UCDchina()
    from glob import glob
    file_list=glob(path.join(CURRNET_PATH, 'ucdchina/*'))
    for f in file_list:
        ucd_china.parse_page(f)
    #fetcher = NoCacheFetch(0, headers=headers)
    #spider = Rolling( fetcher, ucd_china.ucd_url_builder() )
    #spider_runner = GSpider(spider, workers_count=10)
    #spider_runner.start()

if __name__ == '__main__':
    main()
