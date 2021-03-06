USER2RSS = """
10000076 http://feed.uitony.com/
10009225 http://feed43.com/rexsong.xml 
10000066 http://feed.feedsky.com/dreamcog_yo2
10002411 http://www.realfex.com/feed
10000566 http://xlvector.net/blog/?feed=rss2
10066567 http://blog.sina.com.cn/rss/1677574270.xml
10043973 http://blog.sina.com.cn/rss/1593119885.xml
""".strip().split('\n')


USER2RSS = [
    i.split() for i in USER2RSS
]

USER2RSS = [
    (int(i[0]), i[1]) for i in USER2RSS
]

import _env

from model.rss import rss_new, Rss, Reader, GREADER_USERNAME, GREADER_PASSWORD
from zweb.orm import ormiter


for user_id, rss in USER2RSS:
    rss_new(user_id, rss, 0)

reader = Reader(GREADER_USERNAME, GREADER_PASSWORD)

subscription_list = set(reader.subscription_list())


for rss in ormiter(Rss):
    rss_url = rss.url


    if 'feed/%s'%rss_url in subscription_list:
        continue

    print 'subscribe' , rss_url
    reader.subscribe(rss_url)

