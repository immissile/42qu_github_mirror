#coding:utf-8

import _env
from zkit.spider import Rolling, Fetch, NoCacheFetch, GSpider
from json import loads
from kyotocabinet import DB
import sys
from os.path import join, abspath, dirname
from time import time


fetched = DB()
fetched.open(
    join(dirname(abspath(__file__)), "douban_rec_fetched.kch"),
    DB.OWRITER | DB.OCREATE
)

db = DB()
db.open(
    join(dirname(abspath(__file__)), "douban_rec.kch"),
    DB.OWRITER | DB.OCREATE
)

API_KEY = "00d9bb33af90bf5c028d319b0eb23e14"

REC_URL = "http://api.douban.com/people/%%s/recommendations?alt=json&apikey=%s"%API_KEY

LIKE_URL = "http://www.douban.com/j/like?tkind=%s&tid=%s"

NOW = int(time()/60)

def user_id_list_by_like(data, url):
    for i in loads(data):
        id = int(i['id'])
        uid = i['uid']

        if not uid.isdigit():
            db[uid] = id

        url = REC_URL%id

        if id not in fetched:
            fetched[id] = NOW
            yield user_id_list_by_rec, url , id, 1
        else:
            yield user_id_list_by_rec, url , id

def url_id_list_by_rec_all(id):
    start_index = 0
    start_index += 10

def user_id_list_by_rec(data, url, id, start_index=None):
    data = loads(data)
    entry_list = data['entry']
    #print len(entry_list)
    if entry_list:
        for i in entry_list:
            title = i[u'title'][u'$t']
            if title.startswith("推荐"):
                title = title[2:]
            cid = i[u'db:attribute'][0][u'$t']
            print title, cid

        if start_index is not None:
            start = start_index+10
            url = "%s&max-result=10&start-index=%s"%(REC_URL%i, start)
            yield user_id_list_by_rec, url, id, start
        print "---------------------------------------"

def main():
    url_list = [
        (user_id_list_by_like, LIKE_URL%(1015 , 193974547)),
    ]

    headers = {
        'Cookie': 'bid="i9gsK/lU40A"; ll="108288"; __gads=ID=94ec68b017d7ed73:T=1324993947:S=ALNI_MaYLBDGa57C4diSiOVJspHn0IAVQw; __utma=164037162.1587489682.1327387877.1327387877.1327387877.1; __utmz=164037162.1327387877.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); viewed="7153184"; __utmb=164037162.2.8.1327387877; __utmc=164037162; RT=s=1327387895075&r=http%3A%2F%2Fwww.douban.com%2Fnote%2F196951541%2F; dbcl2="13593891:UKKGQFylj18"; ck="lLgF"'

    }

    fetcher = NoCacheFetch(1, headers=headers)
    spider = Rolling( fetcher, url_list )
    spider_runner = GSpider(spider, workers_count=1)
    spider_runner.start()


if __name__ == "__main__":

    main()
    db.close()
    fetched.close()

