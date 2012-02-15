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
    for i in QUESTION_ID_SET:
        yield zhihu_question_parser, 'http://www.zhihu.com/question/%s'%i

how_long = HowLong(len(QUESTION_ID_SET))

def zhihu_topic_title(url , html):
    if '请输入图中的数字：' in html:
        print '请输入图中的数字：'
        return

    r = '<h3>邀请别人回答问题</h3>' in html
    return r

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
        {},
        2.6,
        zhihu_topic_title
    )
    spider = Rolling( fetcher, url_list )

    debug = False
    debug = True

    spider_runner = GSpider(spider, workers_count=3, debug=debug)
    spider_runner.start()

    
spider(zhihu_question_url())

