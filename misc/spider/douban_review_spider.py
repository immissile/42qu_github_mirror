#coding:utf-8
import _env
from zkit.google.greader import Reader
from config import GREADER_USERNAME, GREADER_PASSWORD
from zkit.pprint import pprint

reader = Reader(GREADER_USERNAME, GREADER_PASSWORD)

result = []
for feed in reader.feed("feed/http://book.douban.com/feed/review/book"):
    pprint(feed)
    data = {}
    data['title'] = feed['title']
    data['author'] = feed['author']
    data['content'] = feed['content']
    data['updated'] = feed['updated']
    data['id'] = feed['id']
    data['published'] = feed['published']    
    
    result.append(data)


if __name__ == "__main__":
    pass



