#coding:utf-8


import _env
from model.douban import DOUBAN_REC_CID, douban_rec_new, DoubanUser, Model
from json import loads
from zkit.bot_txt import txt_wrap_by_all, txt_wrap_by
from model.days import int_by_string

API_KEY = '0b28ac78faf4254c217a056af0dc6fe4'

URL_REC = 'http://api.douban.com/people/%%s/recommendations?alt=json&apikey=%s'%API_KEY

URL_LIKE = 'http://www.douban.com/j/like?tkind=%s&tid=%s'

URL_USER_INFO = 'http://api.douban.com/people/%%s?alt=json&apikey=%s'%API_KEY
    
class DoubanFetched(Model):
    pass

def user_id_by_txt(htm):
    r = [
        str(uid).rstrip('/')
        for uid in
        set(txt_wrap_by_all('href="http://www.douban.com/people/', '"', htm))
    ]
    r = [i for i in r if i.isalnum()]
    return r

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

#            for uid in user_id_by_txt(title):
#                yield douban_recommendation_begin_tuple(uid)

            attribute = i[u'db:attribute']
            cid = str(attribute[0][u'$t'])
            if cid in DOUBAN_REC_CID:
                cid = DOUBAN_REC_CID[cid]
                id = i[u'id'][u'$t'].rsplit('/', 1)[1]
                time = i[u'published'][u'$t'].split('+', 1)[0]
                time = int_by_string(time)
                douban_rec_new(
                    id ,
                    user_id, cid, title,
                    time
                )
                from douban_parse import DOUBAN_REC_PARSE
                if cid in DOUBAN_REC_PARSE:
                    _ = DOUBAN_REC_PARSE[cid](title, user_id)
                    if _ is not None:
                        for item in _:
                            yield item

        if start_index is not None:
            start = start_index+10
            url = '%s&max-result=10&start-index=%s'%(URL_REC%user_id, start)
            yield douban_recommendation, url, start
    else:
        f = DoubanFetched.get_or_create(id=user_id)
        f.save()

def douban_recommendation_begin_tuple(id):
    id = str(id)
    if DoubanUser.by_url(id):
        return
    if id in EXIST:
        return
    EXIST.add(id)
    return douban_recommendation, URL_REC%id, 1

def main():
    from zweb.orm import ormiter
    from douban_spider import  spider

    def url_list():
        for i in ormiter(DoubanUser):
            id = i.id
            if DoubanFetched.get(id):
                continue
            yield douban_recommendation, URL_REC%id, 1
            f = DoubanFetched.get_or_create(id=id)
            f.save()

    spider(url_list())

if __name__ == '__main__':

    main()
