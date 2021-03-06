#coding:utf-8
import _env
from os.path import abspath, join
from json import loads
from urllib import quote
from zkit.pprint import pformat
from zhihu_topic_id_rank import ID2RANK
from zkit.spider import Rolling, Fetch, MultiHeadersFetch, GSpider, NoCacheFetch
from zkit.bot_txt import txt_wrap_by, txt_wrap_by_all
from zhihu_topic_url2id_data import URL2ID
from zkit.howlong import HowLong
from urllib import  urlencode


ID2RANK = ID2RANK.items()
ID2RANK.sort(key=lambda x:-x[1])
id2url = dict((v, k) for k, v in URL2ID.items())

QUESTION_ID_SET = set()

def zhihu_topic_url():
    for k, v in ID2RANK:
        if k not in id2url:
            print k, v
            continue
        url = id2url[k]
        url = quote(url)
        yield zhihu_topic_parser, 'http://www.zhihu.com/topic/%s'%url

CACHE_COUNT = 0
FETCH_COUNT = 0
how_long = HowLong(len(ID2RANK))

def zhihu_topic_title(url , html):
    if '请输入图中的数字：' in html:
        print '请输入图中的数字：'
        return

    if 'offset=' in url and '<!doctype'  in html:
        return False

    r = '<h3>你的话题经验</h3>' in html
    #print url, r, html
    if not r:
        r = any((
                '<h3>邀请别人回答问题</h3>' in html,
                '"feed-' in html
            ))
    return r

# [["\u8c46\u74e3\u4e5d\u70b9", "\u8c46\u74e3\u4e5d\u70b9", "http://p1.zhimg.com/a1/78/a178d3f0d_s.jpg", 4717], [["\u8c46\u74e3", "\u8c46\u74e3", "http://p1.zhimg.com/10/59/1059dd38c_s.jpg", 9675]], 1, 0, "", 0]]);
#当前话题 当前话题的父话题

def zhihu_topic_parser(html, url):
    global FETCH_COUNT

    #txt = txt_wrap_by( 'DZMT.push(["current_topic",', ')', html )
    #print loads(txt)[:2][0][0]
    question_id_list = map(int, filter(str.isdigit, txt_wrap_by_all('href="/question/', '">', html)))
    QUESTION_ID_SET.update(question_id_list)
    #QUESTION_ID_SET
    feed_id_list = txt_wrap_by_all('id="feed-', '">', html)
    print feed_id_list
#    for i in feed_id_list:
#        yield zhihu_question_parser, "http://www.zhihu.com/question/%s"%i
    if len(feed_id_list) >= 20:
        last_one = feed_id_list[-1]
        yield zhihu_topic_feed, {'url':url, 'data':urlencode(dict(start=last_one, offset=20))}, 20

#print len(question_id_list), len(feed_id_list)
#for i in question_id_list:
#    yield zhihu_question_parser, 'http://www.zhihu.com/question/%s'%i

#offset = 20
#start = 12624381

def zhihu_topic_feed(html, url, offset):
    o = loads(html)
    #pprint(o)
    id_list = txt_wrap_by_all('id=\\"feed-', '\\"', html)
    question_id_list = txt_wrap_by_all('href=\\"/question/', '\\"', html)
    QUESTION_ID_SET.update(map(int,question_id_list))

    print ">>>", len(QUESTION_ID_SET),'question', how_long.done, how_long.remain, how_long.estimate()

#    for i in id_list:
#        yield zhihu_question_parser, "http://www.zhihu.com/question/%s"%i
#    print id_list
    if len(id_list)>3:
        offset += o['msg'][0]
        yield zhihu_topic_feed, {'url':url['url'], 'data':urlencode(dict(start=id_list[-1], offset=offset))}, offset
    else:
        print "done", how_long.again(), how_long.done, how_long.remain


def zhihu_question_parser(html, url):
#    print url
    pass

COOKIE = (
"""__utma=155987696.1921085572.1329154757.1329154757.1329154757.1; __utmb=155987696.14.9.1329154905385; __utmc=155987696; __utmz=155987696.1329154757.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=155987696.Logged%20In; q_c0=MjIwMDA0fGVHSXZJTFl1ZGxRVHBMSGQ=|1329154797|58efd2296add506f3d88428926aaeae92587a465""",
'__utmz=155987696.1328970860.126.10.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/register; __utma=155987696.922373387.1325132903.1328965603.1328970860.126; __utmv=155987696.Logged%20In; q_c0=MjE4NjYyfFV1YjRvdGczalJFOWlCd0g=|1328973675|4be5e7eae08c14109a129099780c733abe350bba; __utmb=155987696.90.9.1328973170544; __utmc=155987696',
'_xsrf=921952144fdd481582474494f379a7bd; __utma=155987696.322433586.1328975813.1328975813.1328975813.1; __utmb=155987696.64.9.1328977105353; __utmc=155987696; __utmz=155987696.1328975813.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=155987696.Logged%20In; q_c0=MjE4NzM2fExGUUlaOEtTNnp3V2dXWEw=|1328976244|d2ffe0742678bf469312a7fa3638ccbbe70046df',
'__utma=155987696.426164303.1328980648.1329003296.1329007976.3; __utmz=155987696.1329007976.3.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=155987696.Logged%20In; _xsrf=c0ea4fa60d62410983766dda27adfd24; __utmc=155987696; q_c0=MjE4Nzg4fEx4QTlvUlFsdVhGZmJId1g=|1329008428|12e51876ed895fe84c38d7430fd02728cf256a3d',
"""__utma=155987696.426164303.1328980648.1329130544.1329152677.14; __utmz=155987696.1329049453.9.5.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/topic/%E8%AE%A1%E7%AE%97%E7%94%9F%E7%89%A9%E5%AD%A6; __utmv=155987696.Logged%20In; _xsrf=a7839ee1b6124c78b347f54d781c1ace; __utmb=155987696.27.9.1329154417037; __utmc=155987696; q_c0=MjIwMDAzfGFwbm9GbjMxNG5qZkVmSFA=|1329154405|e0e8bef5982dc80930ed1e64ee941b8e186d18fa""",
)


def spider(url_list):
#    fetcher = MultiHeadersFetch(  headers=tuple( { 'Cookie': i } for i in COOKIE))
    fetcher = Fetch(
        '/tmp',
        tuple( { 'Cookie': i } for i in COOKIE),
        2.6,
        zhihu_topic_title
    )
    spider = Rolling( fetcher, url_list )

    debug = False
    debug = True

    spider_runner = GSpider(spider, workers_count=1, debug=debug)
    spider_runner.start()

    global QUESTION_ID_SET
    QUESTION_ID_SET = tuple(QUESTION_ID_SET)
    with open("question_id.py","w") as question:
        question.write("QUESTION_ID_SET = ")
        question.write(pformat(QUESTION_ID_SET))
    
spider(zhihu_topic_url())

