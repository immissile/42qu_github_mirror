#coding:utf-8
import _env
from zkit.google.greader import Reader
from config import GREADER_USERNAME, GREADER_PASSWORD
from zkit.pprint import pprint
from json import loads

reader = Reader(GREADER_USERNAME, GREADER_PASSWORD)


for feed in reader.feed("feed/http://book.douban.com/feed/review/book"):
    pprint(feed)


if __name__ == "__main__":
    pass



