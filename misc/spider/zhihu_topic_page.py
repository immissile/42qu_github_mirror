#coding:utf-8
import _env
import mmseg
from os.path import abspath, dirname, join
from json import loads
from urllib import quote
from zkit.pprint import pformat
from zhihu_topic_data import ZHIHU_TOPIC
from operator import itemgetter
from zkit.spider import Rolling, Fetch, MultiHeadersFetch, GSpider, NoCacheFetch

ZHIHU_TOPIC.sort(key=lambda x:-x[4])

def zhihu_topic_url():
    for i in ZHIHU_TOPIC:
        url = i[2] or i[1]
        url = quote(url)
        yield zhihu_topic_parser, 'http://www.zhihu.com/topic/%s'%url


def zhihu_topic_parser(html, url):
    print html

COOKIE = (
    '__utmz=155987696.1328970860.126.10.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/register; __utma=155987696.922373387.1325132903.1328965603.1328970860.126; __utmv=155987696.Logged%20In; q_c0=MjE4NjYyfFV1YjRvdGczalJFOWlCd0g=|1328973675|4be5e7eae08c14109a129099780c733abe350bba; __utmb=155987696.90.9.1328973170544; __utmc=155987696',

)

def spider(url_list):
#    fetcher = MultiHeadersFetch(  headers=tuple( { 'Cookie': i } for i in COOKIE))
    fetcher = Fetch("/tmp", headers=tuple( { 'Cookie': i } for i in COOKIE)[0])
    spider = Rolling( fetcher, url_list )

    debug = False
    debug = True

    spider_runner = GSpider(spider, workers_count=30, debug=debug)
    spider_runner.start()

spider(zhihu_topic_url())

