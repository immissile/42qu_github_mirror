#coding:utf-8
from json import loads
from model.douban import user_id_by_douban_url, douban_url_user_new, \
CID_DOUBAN_FEED_TOPIC, CID_DOUBAN_FEED_NOTE, douban_rec_new, douban_user_feed_new,\
DOUBAN_REC_CID, CID_DOUBAN_USER_FEED_LIKE , CID_DOUBAN_USER_FEED_REC 
from douban_parse import parse_topic, parse_note 



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


        if not user_id:
            user_id = douban_url_user_new(uid, id, i['screen_name'])
            yield user_id_list_by_rec, url , id, user_id, 1
#        else:
#            yield user_id_list_by_rec, url , id, user_id


        douban_user_feed_new(CID_DOUBAN_USER_FEED_LIKE, cid, rid, user_id)

def fetch_id_by_uid(data, url, uid):
    data = loads(data)
    id = data[u'id'][u'$t'].rsplit("/", 1)[1]
    user_id = user_id_by_douban_url(id)
    if not user_id:
        screen_name = data[u'title'][u'$t']
        user_id = douban_url_user_new(uid, id, screen_name)
        yield user_id_list_by_rec, URL_REC%id , id, user_id, 1


def fetch_user(uid):
    if not uid.isdigit() and not user_id_by_douban_url(uid):
        return fetch_id_by_uid, URL_USER_INFO%uid, uid



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
                    _iter = func(title, user_id)
                    if _iter is not None:
                        for i in _iter:
                            yield i
                else:
                    #print i[u'id'][u'$t'].rsplit("/", 1)[1] , user_id, title 
                    douban_rec_new(
                        i[u'id'][u'$t'].rsplit("/", 1)[1] , 
                        user_id, cid, title
                    )
        if start_index is not None:
            start = start_index+10
            url = "%s&max-result=10&start-index=%s"%(URL_REC%id, start)
            yield user_id_list_by_rec, url, id, user_id, start
