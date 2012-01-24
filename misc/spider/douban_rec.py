#coding:utf-8

import _env
from zkit.spider import Rolling, Fetch, NoCacheFetch, GSpider
from json import loads

API_KEY = "00d9bb33af90bf5c028d319b0eb23e14"

"apikey=%s"%API_KEY

LIKE_URL = "http://www.douban.com/j/like?tkind=%s&tid=%s"

def user_id_list_by_like(data, url):
    for i in loads(data):
        print int(i['id']) , i['uid']


def main():
    url_list = [
        (user_id_list_by_like, LIKE_URL%(1015 , 193974547)),
    ]

    headers = {

        'Cookie': 'bid="i9gsK/lU40A"; ll="108288"; __gads=ID=94ec68b017d7ed73:T=1324993947:S=ALNI_MaYLBDGa57C4diSiOVJspHn0IAVQw; __utma=164037162.1587489682.1327387877.1327387877.1327387877.1; __utmz=164037162.1327387877.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); viewed="7153184"; __utmb=164037162.2.8.1327387877; __utmc=164037162; RT=s=1327387895075&r=http%3A%2F%2Fwww.douban.com%2Fnote%2F196951541%2F; dbcl2="13593891:UKKGQFylj18"; ck="lLgF"'

    }

    fetcher = NoCacheFetch(headers=headers)
    spider = Rolling( fetcher, url_list )
    spider_runner = GSpider(spider, workers_count=1)
    spider_runner.start()


if __name__ == "__main__":
    main()
