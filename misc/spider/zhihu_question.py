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


def zhihu_question_parser(html, url):
    name = txt_wrap_by(
        '<title>',
        ' - 知乎</title>',
        html
    )
    name = unescape(name)
    print name
    print how_long.again(), how_long.remain, how_long.done
    
def zhihu_question_url():
    with open("zhihu_question_to_dump.json") as zhihu_question_dump:
        for line in zhihu_question_dump:
            line = loads(line)
            url = line[1]
            #print line[0]
            yield zhihu_question_parser, url 

how_long = HowLong(67585)

def zhihu_topic_title(url , html):
    #if  'href="/draft">' in html:
    #    return

    if '请输入图中的数字：' in html:
        print '请输入图中的数字： in cache'
        return

    r = '<h3>邀请别人回答问题</h3>' in html
    return r

COOKIE = (
"""_xsrf=da3db09b91514bba9938504036341fe1; __utma=155987696.321760361.1329322590.1329322590.1329322590.1; __utmb=155987696.11.9.1329322707028; __utmc=155987696; __utmz=155987696.1329322590.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=155987696.Logged%20In; q_c0=MjE4NjYyfFV1YjRvdGczalJFOWlCd0g=|1329322681|199897e47544f20d0e26af99f06bb2ef3169ae01""",

"""Cookie: __utma=155987696.225301714.1329322755.1329322755.1329322755.1; __utmb=155987696.4.10.1329322755; __utmc=155987696; __utmz=155987696.1329322755.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=155987696.Logged%20In; q_c0=MjE4NzM2fExGUUlaOEtTNnp3V2dXWEw=|1329322766|6dbbb4c6adbb8c4faa60c5fc84940cc0d9635a8d""",

"""Cookie: _xsrf=3b6911a3e7a14d33b9853c463e6b8967; __utma=155987696.1049756401.1329322821.1329322821.1329322821.1; __utmb=155987696.7.9.1329322838469; __utmc=155987696; __utmz=155987696.1329322821.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=155987696.Logged%20In; q_c0=MjE4Nzg4fEx4QTlvUlFsdVhGZmJId1g=|1329322826|bd290c68d942dd308a43792f7c56a12236c46fc8""",

"""Cookie: __utma=155987696.1049756401.1329322821.1329322821.1329322821.1; __utmb=155987696.13.9.1329322888421; __utmz=155987696.1329322821.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=155987696.Logged%20In; __utmc=155987696; q_c0=MjIwMDAzfGFwbm9GbjMxNG5qZkVmSFA=|1329322886|d8b27e8388545d7b845faa7cdc10adac05420f6d""",

"""Cookie: _xsrf=af5b78fb77e842258c87716af77115c7; __utma=155987696.1623286680.1329322924.1329322924.1329322924.1; __utmb=155987696.4.10.1329322924; __utmc=155987696; __utmz=155987696.1329322924.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=155987696.Logged%20In; q_c0=MjIwMDA0fGVHSXZJTFl1ZGxRVHBMSGQ=|1329322930|a98a0b215fb8dd6f698193149447c98e352ef13c""",

"""Cookie: _xsrf=74d12a578bd942a08c8ed0570b783019; __utma=155987696.1975482818.1329361470.1329361470.1329361470.1; __utmb=155987696.8.10.1329361470; __utmc=155987696; __utmz=155987696.1329361470.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=155987696.Logged%20In; q_c0=NDMwfEUySWpWdVp5cHFGdllGNDI=|1329361485|8d1af7b931c14ef2626bcc431ec75cd094a78bd6""",

)


def spider(url_list):
    fetcher = Fetch(
        '/home/zuroc/tmp',
        tuple( { 'Cookie': i.replace('Cookie:','').strip() } for i in COOKIE),
        25,
        zhihu_topic_title
    )
    spider = Rolling( fetcher, url_list )

    debug = False
    debug = True

    spider_runner = GSpider(spider, workers_count=1, debug=debug)
    spider_runner.start()

    
spider(zhihu_question_url())

