#coding:utf-8


import _env
from model.douban import DOUBAN_REC_CID, douban_rec_new, DoubanUser
from json import loads
from zkit.bot_txt import txt_wrap_by_all, txt_wrap_by
from model.days import int_by_string

API_KEY = '00d9bb33af90bf5c028d319b0eb23e14'

URL_REC = 'http://api.douban.com/people/%%s/recommendations?alt=json&apikey=%s'%API_KEY

URL_LIKE = 'http://www.douban.com/j/like?tkind=%s&tid=%s'

URL_USER_INFO = 'http://api.douban.com/people/%%s?alt=json&apikey=%s'%API_KEY

def user_id_by_txt(htm):
    return [
        str(uid).rstrip('/')
        for uid in
        set(txt_wrap_by_all('href="http://www.douban.com/people/', '"', htm))
    ]


EXIST = set()

def douban_recommendation(data, url, start_index=None):
    data = loads(data)
    entry_list = data[u'entry']

    user_id, url = map(
        str,
        [i['@href'].strip('/').rsplit('/', 1)[-1]
        for i in data[u'author'][u'link'][:2]]
    )
    
    if start_index == 1:
        name = data[u'title'][u'$t'][:-4]
        DoubanUser.new(user_id, url, name)

    if entry_list:
        for i in entry_list:
            title = i[u'content'][u'$t'].replace('\r', ' ').replace('\n', ' ').strip()

            for uid in user_id_by_txt(title):
                yield douban_recommendation_begin_tuple(id)

            attribute = i[u'db:attribute']
            cid = str(attribute[0][u'$t'])
            if cid in DOUBAN_REC_CID:
                id = i[u'id'][u'$t'].rsplit('/', 1)[1]
                time = i[u'published'][u'$t'].split('+', 1)[0]
                time = int_by_string(time)
                douban_rec_new(
                    id ,
                    user_id, cid, title,
                    time
                )

        if start_index is not None:
            start = start_index+10
            url = '%s&max-result=10&start-index=%s'%(URL_REC%user_id, start)
            yield douban_recommendation, url, start

def douban_recommendation_begin_tuple(id):
    if not DoubanUser.by_url(uid):
        return
    if id in EXIST:
        return
    EXIST.add(id)
    return douban_recommendation, URL_REC%id, 1

def main():
    from douban_spider import  spider
    url_list = [
        douban_recommendation_begin_tuple('zuroc')
    ]
    spider(url_list)

if __name__ == '__main__':

    main()
