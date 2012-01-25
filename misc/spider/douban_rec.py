#coding:utf-8

import _env
from zkit.spider import Rolling, Fetch, NoCacheFetch, GSpider
from zkit.bot_txt import txt_wrap_by_all, txt_wrap_by
from json import loads
import sys
from time import time
from kvdb import KvDb

DOUBAN_REC_CID = set("""artist
artist_video
back
book
discussion
doulist
entry
event
group
movie
music
note
online
photo
photo_album
review
site
topic
url""".split())

kvdb = KvDb()

db = kvdb.open_db("rec")
fetch_uid = kvdb.open_db("rec_fetch_uid")
fetch_rec = kvdb.open_db( "fetch_rec")
fetch_like = kvdb.open_db('fetch_like')

API_KEY = "00d9bb33af90bf5c028d319b0eb23e14"

URL_REC = "http://api.douban.com/people/%%s/recommendations?alt=json&apikey=%s"%API_KEY

URL_LIKE = "http://www.douban.com/j/like?tkind=%s&tid=%s"

URL_USER_INFO = "http://api.douban.com/people/%%s?alt=json&apikey=%s"%API_KEY

CID_NOTE = 1015
CID_TOPIC = 1013

NOW = int(time()/60)

def user_id_list_by_like(data, url):
    for i in loads(data):
        id = int(i['id'])
        uid = i['uid']

        if not uid.isdigit():
            db[uid] = id

        url = URL_REC%id

        if id not in fetch_uid:
            fetch_uid[id] = NOW
            yield user_id_list_by_rec, url , id, 1
        else:
            yield user_id_list_by_rec, url , id

def fetch_id_by_uid(data, url, uid):
    data = loads(data)
    id = data[u'id'][u'$t'].rsplit("/", 1)[1]
    db[uid] = id
    if id not in fetch_uid:
        fetch_uid[id] = NOW
        yield user_id_list_by_rec, URL_REC%id , id, 1

def fetch_like_if_new(cid, rid):
    key = "%s:%s"%(cid, rid)
    if key not in fetch_like:
        fetch_like[key] = NOW
        return user_id_list_by_like , URL_LIKE%(cid, rid)

def fetch_if_new(uid):
    if not uid.isdigit() and uid not in db:
        return fetch_id_by_uid, URL_USER_INFO%uid, uid

def url_last(url):
    return url.rstrip("/").rsplit("/", 1)[1]

def parse_topic(title):
    t = [i.split('">', 1) for i in txt_wrap_by_all('<a href="', '</a>', title)]
    group_url , group_name = t[0]
    group_url = url_last(group_url)
    topic_url , topic_name = t[1]
    topic_id = url_last(topic_url)

    result = fetch_like_if_new(CID_TOPIC, topic_id)
    if result:
        #print group_url, group_name, topic_url, topic_name
        yield result
        yield parse_topic_htm , topic_url


def parse_note(title):
    t = [i.split('">', 1) for i in txt_wrap_by_all('<a href="', '</a>', title)]
    uid_url = t[0][0]
    if uid_url.startswith("http://www.douban.com/people/"):
        uid = url_last(uid_url)
        yield fetch_if_new(uid)
    note_url , note_title = t[1]
    note_id = url_last(note_url)
    result = fetch_like_if_new(CID_NOTE, note_id)
    if result:
        yield result
        if note_url.startswith("http://www.douban.com/note/"):
            func = parse_note_people_htm
        elif note_url.startswith("http://site.douban.com/widget/notes/"):
            func = parse_note_site_htm
        else:
            func = 0
        if func:
            yield func , note_url


def parse_title_num_htm(data):
    title = txt_wrap_by("<title>", "</title>", data)
    rec_num = txt_wrap_by('<span class="rec-num">', "人</span>", data) or 0
    like_num = txt_wrap_by('<span class="fav-num" data-tid="', '</a>喜欢</span>', data) or 0
    if like_num:
        like_num = txt_wrap_by('<a href="#">', '人', like_num)
    return title , int(rec_num)+int(like_num)

def parse_topic_htm(data, url):
    title , num = parse_title_num_htm(data)
    htm = txt_wrap_by('<div class="topic-content">', '</div>', data)
    print url , title, num

def parse_note_site_htm(data, url):
    html = txt_wrap_by(' class="note-content"><pre>', "</pre>", data)
    title , num = parse_title_num_htm(data)
    print url , title, num

def parse_note_people_htm(data, url):
    html = txt_wrap_by('<pre class="note">', "</pre>", data)
    title , num = parse_title_num_htm(data)
    print url , title, num


def user_id_list_by_rec(data, url, id, start_index=None):
    data = loads(data)
    entry_list = data['entry']
    if entry_list:
        for i in entry_list:
            title = i[u'content'][u'$t'].replace("\r", " ").replace("\n", " ").strip()
            attribute = i[u'db:attribute']
            cid = str(attribute[0][u'$t'])
            if cid in DOUBAN_REC_CID:
                if cid == "note":
                    func = parse_note
                elif cid == "url":
                    func = 0
                elif cid == "topic":
                    func = parse_topic
                elif cid == "entry":
                    func = 0
                elif cid == "video":
                    func = 0
                else:
                    func = 0

                if func:
                    _iter = func(title)
                    if _iter is not None:
                        for i in _iter:
                            yield i
                else:
                    fetch_rec[ i[u'id'][u'$t'].rsplit("/", 1)[1] ] = "%s %s %s"%(id, cid, title)

        if start_index is not None:
            start = start_index+10
            url = "%s&max-result=10&start-index=%s"%(URL_REC%id, start)
            yield user_id_list_by_rec, url, id, start

def main():
    url_list = [
        (user_id_list_by_like, URL_LIKE%(1015 , 193974547)),
    ]

    headers = {
        'Cookie': 'bid="i9gsK/lU40A"; ll="108288"; __gads=ID=94ec68b017d7ed73:T=1324993947:S=ALNI_MaYLBDGa57C4diSiOVJspHn0IAVQw; __utma=164037162.1587489682.1327387877.1327387877.1327387877.1; __utmz=164037162.1327387877.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); viewed="7153184"; __utmb=164037162.2.8.1327387877; __utmc=164037162; RT=s=1327387895075&r=http%3A%2F%2Fwww.douban.com%2Fnote%2F196951541%2F; dbcl2="13593891:UKKGQFylj18"; ck="lLgF"'

    }

    fetcher = NoCacheFetch( headers=headers)
    spider = Rolling( fetcher, url_list )
    
    debug = False
    debug = True

    spider_runner = GSpider(spider, workers_count=1, debug=debug)
    spider_runner.start()


if __name__ == "__main__":

    main()
    kvdb.close_db()
