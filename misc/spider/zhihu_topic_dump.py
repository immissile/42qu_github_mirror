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


#URL_TEMPLATE = 'http://www.zhihu.com/topic/autocomplete?token=%s&max_matches=999999&use_similar=0'
#这个的rank是关注人数

URL_TEMPLATE = 'http://www.zhihu.com/topic-reg/autocomplete?no_add=1&token=%s&max_matches=9999999&use_similar=0'
#这个的rank是热门回答数

DEFAULT_IMG = '.zhimg.com//e8/2b/e82bab09c_'

from zkit.spider import Rolling, Fetch, GSpider

RESULT = {}

def parse_topic(data, url):
    if 'zhimg.com' not in data:
        return
    #["topic", "百度", "百度", "http://p1.zhimg.com//e7/5e/e75e39ed2_s.jpg", 413, "5854", "baidu"]
    data = loads(data)[0]
    for i in data:
        if i[0] == 'topic' and len(i) > 3:
            tip, url, img , topic_id , rank = i[1:6]

            if DEFAULT_IMG in img:
                img = ''
            else:
                img = str(img).replace('_s.jpg', '_l.jpg')
            if tip == url:
                url = ''
            other_name = set(map(str, i[6:]))
            #if other_name:
            #    print tip
            #    for i in other_name:
            #        print i,
            #    raw_input()
            topic_id = int(topic_id)
            if topic_id not in RESULT:
                RESULT[topic_id] = [
                    str(tip), str(url), img , int(rank), other_name
                ]
            else:
                RESULT[topic_id][-1]|=other_name

def spider(url_list):
    fetcher = Fetch('/tmp')
    spider = Rolling( fetcher, url_list )

    debug = False
    debug = True

    spider_runner = GSpider(spider, debug=debug)
    spider_runner.start()

from operator import itemgetter

if __name__ == '__main__':

#    print u'["topic", "\u767e\u5ea6", "\u767e\u5ea6", "http://p1.zhimg.com//e7/5e/e75e39ed2_s.jpg", 413, "5854", "baidu"]'
    for i in chariter():
        print i
        raw_input()

    raise
    url_list = []
    for i in set(chariter()):
        url_list.append((parse_topic, URL_TEMPLATE%quote(i)))
    spider(url_list)
    RESULT = RESULT.items()
    RESULT.sort(key=itemgetter(0))
    result = []
    for i in RESULT:
        result.append([i[0]])
        result[-1].extend(i[1])
        result[-1][-1] = list(result[-1][-1])

    with open('zhihu_topic_data.py', 'w') as topic:
        topic.write('#coding:utf-8\n')
        topic.write('ZHIHU_TOPIC = ')
        topic.write(pformat(result))



