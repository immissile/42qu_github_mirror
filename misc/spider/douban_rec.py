#coding:utf-8

import _env
from zkit.spider import Rolling, Fetch, NoCacheFetch, GSpider
from zkit.bot_txt import txt_wrap_by_all, txt_wrap_by
from json import loads
import sys
from time import time
from model.douban import user_id_by_douban_url, douban_url_user_new, \
CID_DOUBAN_FEED_TOPIC, CID_DOUBAN_FEED_NOTE, douban_rec_new, douban_user_feed_new,\
douban_feed_new



API_KEY = "00d9bb33af90bf5c028d319b0eb23e14"

URL_REC = "http://api.douban.com/people/%%s/recommendations?alt=json&apikey=%s"%API_KEY

URL_LIKE = "http://www.douban.com/j/like?tkind=%s&tid=%s"

URL_USER_INFO = "http://api.douban.com/people/%%s?alt=json&apikey=%s"%API_KEY

def user_id_list_by_like(data, url, cid, rid):
    for i in loads(data):
        id = int(i['id'])
        uid = i['uid']

        url = URL_REC%id

        user_id = user_id_by_douban_url(id)

        douban_user_feed_new(cid, rid, user_id)

        if not user_id:
            user_id = douban_url_user_new(uid, id, i['screen_name'])
            yield user_id_list_by_rec, url , id, user_id, 1
        else:
            yield user_id_list_by_rec, url , id, user_id

def fetch_id_by_uid(data, url, uid):
    data = loads(data)
    id = data[u'id'][u'$t'].rsplit("/", 1)[1]
    user_id = user_id_by_douban_url(id)
    if not user_id:
        screen_name = ???
        user_id = douban_url_user_new(uid, id, screen_name)
        yield user_id_list_by_rec, URL_REC%id , id, user_id, 1


def fetch_user(uid):
    if not uid.isdigit() and not user_id_by_douban_url(uid):
        return fetch_id_by_uid, URL_USER_INFO%uid, uid

def url_last(url):
    return url.rstrip("/").rsplit("/", 1)[1]

def parse_topic(title):
    t = [i.split('">', 1) for i in txt_wrap_by_all('<a href="', '</a>', title)]
    group_url , group_name = t[0]
    group_url = url_last(group_url)
    topic_url , topic_name = t[1]

    rid = url_last(topic_url)
    cid = CID_DOUBAN_FEED_TOPIC
    
    id = id_by_douban_feed(cid, rid)
    if not id:
        #print group_url, group_name, topic_url, topic_name
        yield user_id_list_by_like , URL_LIKE%(cid, rid), cid, rid
        yield parse_topic_htm , topic_url


def parse_note(title):
    t = [i.split('">', 1) for i in txt_wrap_by_all('<a href="', '</a>', title)]
    uid_url = t[0][0]
    if uid_url.startswith("http://www.douban.com/people/"):
        uid = url_last(uid_url)
        yield fetch_user(uid)
    note_url , note_title = t[1]
    note_id = url_last(note_url)
    cid = CID_DOUBAN_FEED_NOTE
    id = id_by_douban_feed(cid, note_id)
    if not id:
        yield user_id_list_by_like , URL_LIKE%(cid, note_id), cid, note_id

        if note_url.startswith("http://www.douban.com/note/"):
            func = parse_note_people_htm
        elif note_url.startswith("http://site.douban.com/widget/notes/"):
            func = parse_note_site_htm
        else:
            func = 0

        if func:
            yield func , note_url

class ParseHtm(object):
    cid = None

    def htm(self, data):
        return ""

    def user_id(self, data):
        return 0

    def topic_id(self, data):
        return 0

    def __call__(self, data, url):
        rid = url_last(url)
        title = txt_wrap_by("<title>", "</title>", data)
        rec_num = txt_wrap_by('<span class="rec-num">', "人</span>", data) or 0
        like_num = txt_wrap_by('<span class="fav-num" data-tid="', '</a>喜欢</span>', data) or 0
        if like_num:
            like_num = txt_wrap_by('<a href="#">', '人', like_num)

        douban_feed_new(
            self.cid, rid, rec_num, like_num, title, 
            self.htm(data)      ,
            self.user_id(data)  ,
            self.topic_id(data) 
        )       

class ParseTopicHtm(ParseHtm):
    cid = CID_DOUBAN_FEED_TOPIC
    def htm(self, data):
        return txt_wrap_by('<div class="topic-content">', '</div>', data)

parse_topic_htm = ParseTopicHtm()

class ParseNoteSiteHtm(ParseHtm):
    cid = CID_DOUBAN_FEED_NOTE
    def htm(self, data):
        return txt_wrap_by(' class="note-content"><pre>', "</pre>", data)

parse_note_site_htm = ParseNoteSiteHtm()

class ParseNotePeopleHtm(ParseHtm):
    cid = CID_DOUBAN_FEED_NOTE
    def htm(self, data):
        return txt_wrap_by('<pre class="note">', "</pre>", data)

parse_note_people_htm = ParseNotePeopleHtm()


def user_id_list_by_rec(data, url, id, user_id, start_index=None):
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
                    douban_rec_new(
                        i[u'id'][u'$t'].rsplit("/", 1)[1] , 
                        user_id, cid, title
                    )
        if start_index is not None:
            start = start_index+10
            url = "%s&max-result=10&start-index=%s"%(URL_REC%id, start)
            yield user_id_list_by_rec, url, id, user_id, start

def main():
    url_list = [
        (user_id_list_by_like, URL_LIKE%(1015 , 193974547)), 1015, 193974547,
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
