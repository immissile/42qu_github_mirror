#coding:utf-8
import _env
from os.path import abspath, join
from json import loads
from urllib import quote
from zhihu_topic_id_rank import ID2RANK
from zkit.spider import Rolling, Fetch, MultiHeadersFetch, GSpider, NoCacheFetch
from zkit.bot_txt import txt_wrap_by, txt_wrap_by_all
from zhihu_topic_url2id_data import URL2ID
from zkit.howlong import HowLong

ID2RANK = ID2RANK.items()
ID2RANK.sort(key=lambda x:-x[1])
id2url = dict((v, k) for k, v in URL2ID.items())

def zhihu_topic_url():
    for k, v in ID2RANK:
        url = id2url[k]
        url = quote(url)
        yield zhihu_topic_parser, 'http://www.zhihu.com/topic/%s'%url

CACHE_COUNT = 0
FETCH_COUNT = 0
how_long = HowLong(len(ID2RANK))

def zhihu_topic_title(html):
    r = '<h3>相关话题</h3>' in html
    if r:
        how_long.done -= 1
    return r

# [["\u8c46\u74e3\u4e5d\u70b9", "\u8c46\u74e3\u4e5d\u70b9", "http://p1.zhimg.com/a1/78/a178d3f0d_s.jpg", 4717], [["\u8c46\u74e3", "\u8c46\u74e3", "http://p1.zhimg.com/10/59/1059dd38c_s.jpg", 9675]], 1, 0, "", 0]]);
#当前话题 当前话题的父话题

def zhihu_topic_parser(html, url):
    txt = txt_wrap_by( 'DZMT.push(["current_topic",', ')', html )
    global FETCH_COUNT

    print how_long.again(), how_long.done, how_long.remain 
    print loads(txt)[:2][0][0]


COOKIE = (
    '__utmz=155987696.1328970860.126.10.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/register; __utma=155987696.922373387.1325132903.1328965603.1328970860.126; __utmv=155987696.Logged%20In; q_c0=MjE4NjYyfFV1YjRvdGczalJFOWlCd0g=|1328973675|4be5e7eae08c14109a129099780c733abe350bba; __utmb=155987696.90.9.1328973170544; __utmc=155987696',
    '_xsrf=921952144fdd481582474494f379a7bd; __utma=155987696.322433586.1328975813.1328975813.1328975813.1; __utmb=155987696.64.9.1328977105353; __utmc=155987696; __utmz=155987696.1328975813.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=155987696.Logged%20In; q_c0=MjE4NzM2fExGUUlaOEtTNnp3V2dXWEw=|1328976244|d2ffe0742678bf469312a7fa3638ccbbe70046df',
    '__utma=155987696.426164303.1328980648.1329003296.1329007976.3; __utmz=155987696.1329007976.3.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=155987696.Logged%20In; _xsrf=c0ea4fa60d62410983766dda27adfd24; __utmc=155987696; q_c0=MjE4Nzg4fEx4QTlvUlFsdVhGZmJId1g=|1329008428|12e51876ed895fe84c38d7430fd02728cf256a3d',
)

def spider(url_list):
#    fetcher = MultiHeadersFetch(  headers=tuple( { 'Cookie': i } for i in COOKIE))
    fetcher = Fetch(
        '/tmp',
        tuple( { 'Cookie': i } for i in COOKIE),
        3.33,
        zhihu_topic_title
    )
    spider = Rolling( fetcher, url_list )

    debug = False
    debug = True

    spider_runner = GSpider(spider, workers_count=1, debug=debug)
    spider_runner.start()

spider(zhihu_topic_url())

