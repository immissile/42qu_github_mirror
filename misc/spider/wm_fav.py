#coding:utf-8
from json import loads
from json import dumps
import _env
from os.path import abspath, dirname, join
from urllib import quote
from zkit.pprint import pformat, pprint
from operator import itemgetter
from zkit.spider import Rolling, Fetch, MultiHeadersFetch, GSpider, NoCacheFetch
from zkit.bot_txt import txt_wrap_by, txt_wrap_by_all
from zkit.howlong import HowLong
from zkit.htm2txt import unescape


COOKIE = """auid=tpDh6RcYTnSzopBC64smkOG0wK6N%2B4hf; __utma=264742537.1854618108.1331049812.1331889152.1331919387.4; __utmz=264742537.1331049812.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); uid=ARSq0YH%2Fiaugt%2BRnLL7t6AbWY%2FOEOjsvPGq5H4oBArFO1Lg9deFTxm6vPgpm1XmFZA%3D%3D; JSESSIONID=B0F0E2108C1BC6F915C07E0B7CBF8F25.web-15; __utmb=264742537.31.10.1331919387; __utmc=264742537"""

EXIST_ID = set()
USER_DICT = dict()

def wm_parser(html, url):
    user= txt_wrap_by("&u=","&",url)
    #print user
    time = txt_wrap_by('<li id="maxActionTimeInMs"  m="', '"', html)
    if time and 'm='+time not in url and int(time) > 0:
        yield wm_parser, url[:url.rfind('=')+1]+str(time)

    for i in txt_wrap_by_all(' itemid="', '<p class="operating">', html):
        if 'class="content"' in i:
            id = i[:i.find('"')]
            if user not in USER_DICT:
                USER_DICT[user] = set()
            USER_DICT[user].add(id)
            if id not in EXIST_ID:
                yield wm_txt_parser, "http://www.wumii.com/reader/article?id=%s"%id


def wm_txt_parser(html, url):
    id = url.rsplit("=")[-1]
    title =  txt_wrap_by('target="_blank">','</a></p>',html)
    source = txt_wrap_by('">来自：','<', html)
    link = txt_wrap_by(
        'href="',
        '"',
        txt_wrap_by('<p class="info','</p>', html)
    )
    like = txt_wrap_by(
        'class="num-likeIt">',
        '人喜欢</a>',
        html
    )
    txt = txt_wrap_by(
        '<div class="content">',
       ' <p class="operating">',
        html 
    )

    time = txt_wrap_by('<span class="time">','</span>',html)
    #print time       
    data = dumps([
        id,
        like,
        title,
        source,
        link,
        time,
        txt,
    ])
    output.write(data)
    output.write("\n")
        

def spider(url_list):
    fetcher = NoCacheFetch(
        0,
        {
            'Cookie': COOKIE
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
    (wm_parser, 'http://www.wumii.com/user/article/get?type=LIKED_ITEM&u=zuroc&m=9331724404885') ,
]
with open("wm_rec.txt","w") as output:
    spider(url_list)

with open("wm_user_rec.txt","w") as output:
    output.write(dumps(tuple((k,tuple(v)) for k,v in USER_DICT.iteritems())))    


