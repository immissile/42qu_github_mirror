#coding:utf-8

import _env
from zkit.bot_txt import txt_wrap_by_all, txt_wrap_by
from model.douban import douban_feed_new, id_by_douban_feed, douban_user_feed_new, CID_DOUBAN_FEED_REC

def url_last(url):
    return url.rstrip("/").rsplit("/", 1)[1]

def parse_topic(title, user_id):
    t = [i.split('">', 1) for i in txt_wrap_by_all('<a href="', '</a>', title)]
    group_url , group_name = t[0]
    group_url = url_last(group_url)
    topic_url , topic_name = t[1]

    rid = url_last(topic_url)
    cid = CID_DOUBAN_FEED_TOPIC
    
    id = id_by_douban_feed(cid, rid)
    if not id:
        yield user_id_list_by_like , URL_LIKE%(cid, rid), cid, rid
        yield parse_topic_htm , topic_url, user_id


def parse_note(title, user_id):
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

    def __call__(self, data, url, user_id):
        rid = url_last(url)
        douban_user_feed_new(CID_DOUBAN_FEED_REC, rid, user_id)
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
