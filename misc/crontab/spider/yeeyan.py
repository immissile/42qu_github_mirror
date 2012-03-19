#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import _env
import urllib2
from zkit.htm2txt import htm2txt
from zkit.bot_txt import txt_wrap_by_all, txt_wrap_by
from zkit.spider import Rolling, Fetch, NoCacheFetch, GSpider
from time import sleep
from os.path import exists
import os.path
from yajl import dumps
from hashlib import md5
import threading
from zkit.lock_file import LockFile
from writer import Writer,CURRNET_PATH,Spider, url_is_fetched,Spider

class Yeeyan(object):
    def __init__(self):
        pass

    def name_builder(self,url):
        return os.path.join(CURRNET_PATH,"yeeyan", md5(url).hexdigest())

    def yeeyan_crawl(self):
        for page in xrange(1, 5001):
            yield self.parse_index, 'http://article.yeeyan.org/list_a?page=%s'%str(page)

    def parse_page(self,filepath):
        with open(filepath) as f:
            page = f.read()

            title = txt_wrap_by('<title>译言网 | ', '</ti', page)
            tags_wrapper = txt_wrap_by('wumiiTags = "', '"', page)
            tags = tags_wrapper.split(',')
            author = txt_wrap_by('<h2 id="user_info"', '/a', page)
            author = txt_wrap_by('">','<',author)
            rating = txt_wrap_by('已有<span class="number">', '</span', page)
            content_wrapper = txt_wrap_by('id="conBox">','<div class="article_content">',page)
            url = txt_wrap_by('wumiiPermaLink = "','"',page)
            if content_wrapper:
                content,pic_list = htm2txt(content_wrapper)
            else:
                return 

            content = str(content)

            reply_wrapper_list = txt_wrap_by_all('class="comment_content">', '</ul', page)
            reply_list = []
            for reply_wrapper in reply_wrapper_list:
                reply_list.append(txt_wrap_by('<p>', '</p', reply_wrapper))

            Spider.insert(title, tags, content, author, rating ,url, reply_list, pic_list)

            #writer = Writer.get_instance()
            #writer = writer.choose_writer('yeeyan.data')
            #writer.write(out+'\n')

    def save_page(self,page,url):
        filename = self.name_builder(url)
        with open(filename,'w') as f:
            f.write(page)
        self.parse_page(filename)

    def parse_index(self,page, url):
        print "!"
        link_wrapper_list = txt_wrap_by_all('<h5 clas', '</h5', page)
        link_list = []
        for link_wrapper in link_wrapper_list:
            url = txt_wrap_by('href="', '"', link_wrapper)
            filename = self.name_builder(url)
            if not url_is_fetched(url):
                yield self.save_page, url
            else:
                self.parse_page(filename)

    def yeeyan_daily(self):
        yield self.parse_index,'http://article.yeeyan.org/list_a?page=1'


    def yeeyan_cache_walker(self):
        from glob import  glob
        for file_name in glob(join(CURRNET_PATH,'yeeyan','*')):
            self.parse_page(file_name)

def main():
    headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Language':'en,en-US;q=0.8,zh-CN;q=0.6,zh;q=0.4',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Host':'www.zhihu.com',
            'Referer:http':'//www.zhihu.com/',
            'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11',
    }
    new_yeeyan = Yeeyan()
    fetcher = NoCacheFetch(0, headers=headers)
    spider = Rolling( fetcher, new_yeeyan.yeeyan_daily())
    spider_runner = GSpider(spider, workers_count=100)
    spider_runner.start()

if __name__ == '__main__':
    main()
