#coding:utf-8
import _env
from os.path import abspath, join
from json import loads
from zkit.pprint import pformat
from zhihu_topic_data import ZHIHU_TOPIC



#URL_TEMPLATE = 'http://www.zhihu.com/topic/autocomplete?token=%s&max_matches=999999&use_similar=0'
#这个的rank是关注人数

URL_TEMPLATE = 'http://www.zhihu.com/topic/related?tid=%s'
#这个的rank是热门回答数


from zkit.spider import Rolling, Fetch, GSpider

RESULT = {}
TOPIC = {}
def parse_topic(data, url, id):
    RESULT[id] = li = []
    for i in loads(data):
        id = i[3]
        li.append(id)
        TOPIC[id] = map(str, (i[0], i[1], i[2], i[4]))

def spider(url_list):
    fetcher = Fetch('/tmp')
    spider = Rolling( fetcher, url_list )

    debug = False
    debug = True

    spider_runner = GSpider(spider, workers_count=1, debug=debug)
    spider_runner.start()

from operator import itemgetter

if __name__ == '__main__':

#    print u'["topic", "\u767e\u5ea6", "\u767e\u5ea6", "http://p1.zhimg.com//e7/5e/e75e39ed2_s.jpg", 413, "5854", "baidu"]'


    url_list = []
    for t in ZHIHU_TOPIC:
        i = t[0]
        url_list.append((parse_topic, URL_TEMPLATE%i, i))

    spider(url_list)

    with open('zhihu_topic_related_data.py', 'w') as topic:
        topic.write('#coding:utf-8\n')
        topic.write('TOPIC_RELATED = ')
        topic.write(pformat(RESULT))
        topic.write('TOPIC = ')
        topic.write(pformat(TOPIC))



