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
from zhihu_question_id import QUESTION_ID_SET
from zkit.htm2txt import unescape, htm2txt
from yajl import dumps

RESULT = []

def zhihu_question_parser(html, url):
    name = txt_wrap_by(
        '<title>',
        ' - 知乎</title>',
        html
    )
    name = unescape(name)
    if  '<h3>邀请别人回答问题</h3>' in html:
        answer_count = txt_wrap_by('<span id="xhrw">', ' 个答案</span>', html)
    else:
        answer_count = txt_wrap_by('<h3 style="margin: 0 0 5px;">', ' 个答案</', html)

    tag = map(unescape, txt_wrap_by_all('<a class="xjl" href="javascript:;">', '</a>', html))
    #print tag[0]
    answer_count =  int(answer_count or 0)

    if answer_count:
        txt = filter(bool, txt_wrap_by_all('<div class="xmrw">','</div>', html))
        if not txt:
            print url
            print name
            #raw_input()
        else:
            print txt[0]
    else:
        if "个答案" in html and ("0 个答案" not in html) and "还没有答案" not in html:
            print url
            print html 
            #raw_input()
        txt = []

    RESULT.append((answer_count, url, name, tag, [htm2txt(i) for i in txt]))

    print how_long.again(), how_long.remain, how_long.done

def zhihu_question_url():
    for i in QUESTION_ID_SET:
        yield zhihu_question_parser, 'http://www.zhihu.com/question/%s'%i

how_long = HowLong(len(QUESTION_ID_SET))

def zhihu_topic_title(url , html):
    if '请输入图中的数字：' in html:
        print '请输入图中的数字：'
        return

    r = '<h3>邀请别人回答问题</h3>' in html
    if not r:
        r = '>已有帐号了？请登录</h' in html

    return r

def spider(url_list):
#    fetcher = MultiHeadersFetch(  headers=tuple( { 'Cookie': i } for i in COOKIE))
    fetcher = Fetch(
        '/tmp',
    #    tuple( { 'Cookie': i } for i in COOKIE),
        {},
        0, #2.6,
        zhihu_topic_title
    )
    spider = Rolling( fetcher, url_list )

    debug = False
    debug = True

    spider_runner = GSpider(spider, workers_count=3, debug=debug)
    spider_runner.start()


spider(zhihu_question_url())
RESULT.sort(key=lambda x:-x[0])

with open('zhihu_question_dumped.json', 'w') as dumped:
    with open('zhihu_question_to_dump.json', 'w') as to_dump:
        for i in RESULT:
            if i[0] > len(i[-1]):
                to_dump.write(dumps(i)+"\n")
            else:
                dumped.write(dumps(i)+"\n")


