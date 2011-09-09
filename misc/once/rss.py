USER2RSS = """
10009225 http://feed43.com/rexsong.xml 


""".strip().split('\n')


USER2RSS = [
    i.split() for i in USER2RSS
]

USER2RSS = [
    (int(i[0]),i[1]) for i in USER2RSS
]

import _env

from model.rss import rss_new, Rss, Reader, GREADER_USERNAME, GREADER_PASSWORD 
from zweb.orm import ormiter


for user_id, rss in USER2RSS:
    rss_new(user_id, rss) 

reader = Reader(GREADER_USERNAME, GREADER_PASSWORD)

subscription_list =  set(reader.subscription_list())


for rss in ormiter(Rss):
    rss_url = rss.url
    

    if "feed/%s"%rss_url in subscription_list:
        continue
    

    reader.subscribe(rss_url)

