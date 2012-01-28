#coding:utf-8


import _env
from douban_spider import URL_REC, spider
from model.douban import DOUBAN_REC_CID, douban_rec_new
from json import loads
from zkit.bot_txt import txt_wrap_by_all, txt_wrap_by

def user_id_by_txt(htm):
    return [
        str(uid).rstrip("/")
        for uid in 
        set(txt_wrap_by_all('href="http://www.douban.com/people/','"',htm))
    ]


EXIST = set()

def douban_recommendation(data, url, start_index=None):
    data = loads(data)
    entry_list = data['entry']

    user_id, url = map(str,[i['@href'].strip('/').rsplit('/', 1)[-1] for i in data[u'author'][u'link'][:2]])
    
    EXIST.add(user_id)
    EXIST.add(url)

    if entry_list:
        for i in entry_list:
            title = i[u'content'][u'$t'].replace('\r', ' ').replace('\n', ' ').strip()

            for uid in user_id_by_txt(title):
                if uid not in EXIST:
                    EXIST.add(uid)
                    #yield douban_recommendation, URL_REC%uid, 1

            attribute = i[u'db:attribute']
            cid = str(attribute[0][u'$t'])
            if cid in DOUBAN_REC_CID:
                id = i[u'id'][u'$t'].rsplit('/', 1)[1]
                douban_rec_new(
                    id ,
                    user_id, cid, title
                )
    
        if start_index is not None:
            start = start_index+10
            url = "%s&max-result=10&start-index=%s"%(URL_REC%user_id, start)
            yield douban_recommendation, url, start

def main():
    url_list = [
        ( douban_recommendation, URL_REC%'zuroc', 1),
    ]
    spider(url_list)

if __name__ == '__main__':

    main()
