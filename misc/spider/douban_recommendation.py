#coding:utf-8


import _env
from douban_spider import URL_REC, spider
from model.douban import DOUBAN_REC_CID, douban_rec_new

def douban_recommendation(data, url, start_index=None):
    print data 
    data = loads(data)
    entry_list = data['entry']
    print data[u'author']
    return
    if entry_list:
        for i in entry_list:
            title = i[u'content'][u'$t'].replace("\r", " ").replace("\n", " ").strip()
            attribute = i[u'db:attribute']
            cid = str(attribute[0][u'$t'])
            if cid in DOUBAN_REC_CID:
                douban_rec_new(
                    i[u'id'][u'$t'].rsplit("/", 1)[1] , 
                    user_id, cid, title
                )
def main():
    url_list = [
        ( douban_recommendation, URL_REC%"zuroc", 1), 
    ]
    spider(url_list)

if __name__ == "__main__":

    main()
