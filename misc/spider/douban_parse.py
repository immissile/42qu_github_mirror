#coding:utf-8

import _env
from json import loads
from zkit.bot_txt import txt_wrap_by_all, txt_wrap_by
from model.douban import douban_feed_new, id_by_douban_feed, douban_user_feed_new,\
CID_DOUBAN_USER_FEED_REC, CID_DOUBAN_FEED_TOPIC, CID_DOUBAN_FEED_NOTE,\
user_id_by_douban_url, douban_url_user_new 

def url_last(url):
    return url.rstrip("/").rsplit("/", 1)[1]

class ParseRec(object):
    cid = None
    
    def func_url(self, title):
        return (None, "") 

    def __call__(self, title, user_id):
        cid = self.cid
        
        func , url = self.func_url(title)
        rid = url_last(url)
        id = id_by_douban_feed(cid, rid)

        if not id and func:
            from douban_like import user_id_list_by_like, URL_LIKE
            yield user_id_list_by_like , URL_LIKE%(cid, rid), cid, rid
            yield func , url, user_id
        else:
            douban_user_feed_new(CID_DOUBAN_USER_FEED_REC, rid, user_id)
       
class ParseRecTopic(ParseRec):
    cid = CID_DOUBAN_FEED_TOPIC

    def func_url(self, title):
        t = [i.split('">', 1) for i in txt_wrap_by_all('<a href="', '</a>', title)]
        url , topic_name = t[1]
        return parse_topic_htm, url

parse_topic = ParseRecTopic()


class ParseRecNote(ParseRec):
    cid = CID_DOUBAN_FEED_NOTE

    def func_url(self, title):
        t = [i.split('">', 1) for i in txt_wrap_by_all('<a href="', '</a>', title)]
        url , note_title = t[1]

        if url.startswith("http://www.douban.com/note/"):
            func = parse_note_people_htm
        elif url.startswith("http://site.douban.com/widget/notes/"):
            func = parse_note_site_htm
        else:
            func = 0
        return func, url

parse_note = ParseRecNote()

 


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

        _owner_id = self.user_id(data)
        if _owner_id:
            owner_id = user_id_by_douban_url(_owner_id)

            if not owner_id:
                from douban_like import fetch_user 
                yield fetch_user(_owner_id)
            
            owner_id = user_id_by_douban_url(_owner_id)

        douban_feed_new(
            self.cid, rid, rec_num, like_num, title, 
            self.htm(data)      ,
            owner_id  ,
            self.topic_id(data) 
        )       
        for uid in set(txt_wrap_by_all('href="http://www.douban.com/people/','"',data)):
            uid = uid.rstrip('/')
            from douban_like import fetch_user 
            yield fetch_user(uid)

class ParseTopicHtm(ParseHtm):
    cid = CID_DOUBAN_FEED_TOPIC
    def htm(self, data):
        return txt_wrap_by('<div class="topic-content">', '</div>', data)

    def user_id(self, data):
        line = txt_wrap_by('<div class="user-face">','">',data)
        line = txt_wrap_by('"http://www.douban.com/people/','/',line)
        return line

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

    def user_id(self, data):
        line = txt_wrap_by('<div class="pic">','">',data)
        line = txt_wrap_by('"http://www.douban.com/people/','/',line)
        return line


parse_note_people_htm = ParseNotePeopleHtm()

