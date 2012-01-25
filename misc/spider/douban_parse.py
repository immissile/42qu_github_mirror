#coding:utf-8

import _env
from zkit.bot_txt import txt_wrap_by_all, txt_wrap_by
from model.douban import douban_feed_new, id_by_douban_feed, douban_user_feed_new, CID_DOUBAN_USER_FEED_REC

def url_last(url):
    return url.rstrip("/").rsplit("/", 1)[1]


def _parse_result(user_id, cid,  url):
    rid = url_last(url)
    id = id_by_douban_feed(cid, rid)

    if not id:
        yield user_id_list_by_like , URL_LIKE%(cid, rid), cid, rid
        
        func = 0

        if cid == CID_DOUBAN_FEED_NOTE:
            if url.startswith("http://www.douban.com/note/"):
                func = parse_note_people_htm
            elif url.startswith("http://site.douban.com/widget/notes/"):
                func = parse_note_site_htm
        elif cid == CID_DOUBAN_FEED_TOPIC:    
            func = parse_topic_htm

        if func:
            yield func , url, user_id
    else:
        douban_user_feed_new(CID_DOUBAN_USER_FEED_REC, rid, user_id)
        
def parse_topic(title, user_id):
    t = [i.split('">', 1) for i in txt_wrap_by_all('<a href="', '</a>', title)]
    url , topic_name = t[1]
    return _parse_result(user_id, CID_DOUBAN_FEED_TOPIC, url)

def parse_note(title, user_id):
    t = [i.split('">', 1) for i in txt_wrap_by_all('<a href="', '</a>', title)]
    url , note_title = t[1]
    return _parse_result(user_id, CID_DOUBAN_FEED_NOTE,  url)

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
        douban_user_feed_new(CID_DOUBAN_USER_FEED_REC, rid, user_id)
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
        for uid in set(txt_wrap_by_all('href="http://www.douban.com/people/','"',data)):
            print "uid" , "..."
            yield fetch_user(uid)

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

