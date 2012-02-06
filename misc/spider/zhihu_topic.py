#coding:utf-8
import _env
import mmseg
from os.path import abspath, dirname, join
from json import loads

filepath = join(dirname(abspath(mmseg.__file__)), 'data/chars.dic')
def chariter():
    with open(filepath) as charline:
        for i in charline:
            i = i.strip().split()
            if len(i) == 2:
                yield i[-1]

URL_TEMPLATE = 'http://www.zhihu.com/topic/autocomplete?token=%s&max_matches=999999&use_similar=0'


from zkit.spider import Rolling, Fetch, GSpider

def parse_topic(data, url):
    data = loads(data)
    print data
    print len(data)


def spider(url_list):
    fetcher = Fetch("/tmp")
    spider = Rolling( fetcher, url_list )

    debug = False
    debug = True

    spider_runner = GSpider(spider, workers_count=1, debug=debug)
    spider_runner.start()



if __name__ == '__main__':
    url_list = []
    url_list.append((parse_topic, URL_TEMPLATE%'a'))
    spider(url_list)
    pass


