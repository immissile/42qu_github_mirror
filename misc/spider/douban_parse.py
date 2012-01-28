#coding:utf-8

import _env
from json import loads
from zkit.bot_txt import txt_wrap_by_all, txt_wrap_by
from model.douban import douban_feed_new, id_by_douban_feed, douban_user_feed_new,\
DOUBAN_USER_FEED_VOTE_REC, CID_DOUBAN_FEED_TOPIC, CID_DOUBAN_FEED_NOTE,\
DOUBAN_REC_CID, DoubanUser, DOUBAN_USER_FEED_VOTE_LIKE, DoubanFeedOwner
from douban_recommendation import douban_recommendation_begin_tuple, URL_LIKE, user_id_by_txt


def parse_like(data, url, cid, rid):
    for i in loads(data):
        id = int(i[u'id'])

        yield douban_recommendation_begin_tuple(id)

        douban_user_feed_new(DOUBAN_USER_FEED_VOTE_LIKE, cid, rid, id)

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
            yield parse_like , URL_LIKE%(cid, rid), cid, rid
            yield func , url
        else:
            douban_user_feed_new(DOUBAN_USER_FEED_VOTE_REC, cid, rid, user_id)
       
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

    def title(self, data):
        title = txt_wrap_by("<title>", "</title>", data)
        return title

    def __call__(self, data, url):
        rid = url_last(url)

        title = self.title(data)

        rec_num = txt_wrap_by('<span class="rec-num">', "人</span>", data) or 0
        like_num = txt_wrap_by('<span class="fav-num" data-tid="', '</a>喜欢</span>', data) or 0
        if like_num:
            like_num = txt_wrap_by('<a href="#">', '人', like_num)

        _topic = _owner = 0
        
        owner_id = self.user_id(data)
        try:
            owner_id = int(owner_id)
        except ValueError:
            _owner_id = DoubanUser.by_url(owner_id)
            if _owner_id:
                owner_id = _owner_id
            else:
                _owner = owner_id
                owner_id = 0

        topic_id = self.topic_id(data)
        try:
            topic_id = int(topic_id)
        except ValueError:
            _topic = topic_id
            topic_id = 0

        feed_id = douban_feed_new(
            self.cid, 
            rid, 
            rec_num, 
            like_num, 
            title, 
            self.htm(data),
            owner_id  ,
            topic_id
        )      
        if _owner or _topic:
            DoubanFeedOwner(id=feed_id, topic=_topic, owner=_owner).save()

        for user_id in user_id_by_txt(data):
            yield douban_recommendation_begin_tuple(user_id)

class ParseTopicHtm(ParseHtm):
    cid = CID_DOUBAN_FEED_TOPIC
    def htm(self, data):
        result = [ ]
        html = txt_wrap_by('<div class="topic-content">', '</div>', data)
        if html:
            result.append(html)
        user_id = self.user_id(data)
        topic_reply =  txt_wrap_by('<ul class="topic-reply">','</ul>',data)
        topic_reply =  txt_wrap_by_all(' <div class="reply-doc">',' class="lnk-reply">回应</a>',topic_reply)
        
        for i in topic_reply:
            owner_id = txt_wrap_by('<div class="bg-img-green">','</h4>',i)
            owner_id = txt_wrap_by('<a href="http://www.douban.com/people/','/">',owner_id)
            if owner_id!=user_id:
                break
            result.append(txt_wrap_by('</div>','<div class="operation_div"',i)) 
                    
        return '\n'.join(result)

    def user_id(self, data):
        line = txt_wrap_by('<div class="user-face">','">',data)
        line = txt_wrap_by('"http://www.douban.com/people/','/',line)
        return line

    def topic_id(self, data):
        line = txt_wrap_by('<div class="aside">','">回',data)
        line = txt_wrap_by('"http://www.douban.com/group/','/',line)
        return line
    
    def title(self, data):
        title = txt_wrap_by('<tr><td class="tablelc"></td><td class="tablecc"><strong>标题：</strong>','</td>', data)
        if not title:
            title = txt_wrap_by("<title>", "</title>", data)
        return title

parse_topic_htm = ParseTopicHtm()

class ParseNoteSiteHtm(ParseHtm):
    cid = CID_DOUBAN_FEED_NOTE
    def htm(self, data):
        return txt_wrap_by(' class="note-content"><pre>', "</pre>", data)

    def topic_id(self, data):
        line = txt_wrap_by('<div class="sp-logo">','" ',data)
        line = txt_wrap_by('http://site.douban.com/widget/notes/','/',line) 
        return line

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

DOUBAN_REC_PARSE = {
    DOUBAN_REC_CID['note']:parse_note,
    DOUBAN_REC_CID['topic']:parse_topic,
}

if __name__ == "__main__":
    html = """ """

    
    print parse_topic_htm.htm(html)
