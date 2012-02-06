#coding:utf-8
import _env
import mmseg
from os.path import abspath, dirname, join
from json import loads
from urllib import quote
from zkit.pprint import pformat

filepath = join(dirname(abspath(mmseg.__file__)), 'data/chars.dic')
def chariter():
    for i in '0123456789abcdefghijklmnopqrstuvwxyz':
        yield i
    with open(filepath) as charline:
        for i in charline:
            i = i.strip().split()
            if len(i) == 2:
                yield i[-1]


URL_TEMPLATE = 'http://www.zhihu.com/topic/autocomplete?token=%s&max_matches=999999&use_similar=0'
DEFAULT_IMG = 'http://p1.zhimg.com//e8/2b/e82bab09c_s.jpg'

from zkit.spider import Rolling, Fetch, GSpider

RESULT = []

def parse_topic(data, url):
    if 'zhimg.com' not in data:
        return
    data = loads(data)[0]
    for i in data:
        if i[0] == 'topic' and len(i) > 3:
            tip, url, img , topic_id , rank = i[1:]
            if img == DEFAULT_IMG:
                img = None
            if tip == url:
                url = ''
            RESULT.append((topic_id , tip, url, img ,  int(rank)))

def spider(url_list):
    fetcher = Fetch('/tmp')
    spider = Rolling( fetcher, url_list )

    debug = False
    debug = True

    spider_runner = GSpider(spider,  debug=debug)
    spider_runner.start()



if __name__ == '__main__':
    url_list = []
    for i in set(chariter()):
        url_list.append((parse_topic, URL_TEMPLATE%quote(i)))
    spider(url_list)
    with open("zhihu_topic_data.py","w") as topic:
        topic.write("ZHIHU_TOPIC = ")
        topic.write(pformat(RESULT))


