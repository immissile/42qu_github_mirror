#coding:utf-8
import _env
from os.path import abspath, dirname, join
from json import loads
from urllib import quote
from zkit.pprint import pformat, pprint
from operator import itemgetter
from zkit.spider import Rolling, Fetch, MultiHeadersFetch, GSpider, NoCacheFetch
from zkit.bot_txt import txt_wrap_by, txt_wrap_by_all
from zkit.howlong import HowLong
from zkit.htm2txt import unescape 



COOKIE = """auid=tpDh6RcYTnSzopBC64smkOG0wK6N%2B4hf; __utma=264742537.1854618108.1331049812.1331889152.1331919387.4; __utmz=264742537.1331049812.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); uid=ARSq0YH%2Fiaugt%2BRnLL7t6AbWY%2FOEOjsvPGq5H4oBArFO1Lg9deFTxm6vPgpm1XmFZA%3D%3D; JSESSIONID=B0F0E2108C1BC6F915C07E0B7CBF8F25.web-15; __utmb=264742537.31.10.1331919387; __utmc=264742537"""

EXIST_USER = set()
REAL_USER = set()

def wm_parser(html, url):
    if "&p=" not in url:
        REAL_USER.add(url.rsplit("=",1)[-1])
        page_id = txt_wrap_by_all(' pageid="','"',html)
        if page_id:
            page_id = int(page_id[-1])
            for i in xrange(1,page_id+1):
                yield wm_parser, url+"&p=%s"%i 
         
    for user_name in txt_wrap_by_all(' href="/user/','"', html):
        if "/" not in user_name:
            if (user_name in EXIST_USER) or (user_name in REAL_USER):
                continue
            EXIST_USER.add(user_name)
            yield wm_parser , "http://www.wumii.com/user/list/followings?u=%s"%user_name
            yield wm_parser , "http://www.wumii.com/user/list/fans?u=%s"%user_name 


def spider(url_list):
    fetcher = NoCacheFetch(
        0,
        {
            "Cookie": COOKIE
        }
        #'/home/zuroc/tmp',
        #tuple( { 'Cookie': i.replace('Cookie:','').strip() } for i in COOKIE),
        #1,
    )
    spider = Rolling( fetcher, url_list )

    debug = False
    debug = True

    spider_runner = GSpider(spider, workers_count=1, debug=debug)
    spider_runner.start()


    
url_list = [
    (wm_parser, "http://www.wumii.com/user/list/fans?u=trumanlam") , 
    (wm_parser, "http://www.wumii.com/user/list/followings?u=trumanlam") , 
]
spider(url_list)

with open("wm_user.txt", "w") as wm_user:
    for i in REAL_USER:
        wm_user.write("%s\n"%i) 
    
