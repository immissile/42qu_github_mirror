#coding:utf-8
import _env
from idf import Idf
from config import ZDATA_PATH
from os.path import join, exists
from yajl import loads

ZDATA_PATH_TRAIN_IDF = join(ZDATA_PATH, "train/idf")

def train(filename, parser):
    idf = Idf()
    path = join(ZDATA_PATH_TRAIN_IDF, filename)

    tofile = "%s.idf"%path
    if exists(tofile):
        return

    count = 0
    with open(path) as f:
        for txt in parser(f):
            idf.append(txt)
            if count%1000 == 1:
                print filename, count
            count += 1

    idf.tofile(tofile)

def douban_review_parser(review):
    result = []

    for line in review:
        line = line.strip()
        if not line:
            continue
        if line.startswith(">->->"):
            if result:
                line = line.split(" ", 5)
                result.append(line[-1])
                txt = "\n".join(result)
                yield txt
            result = []
        else:
            result.append(line)

def zhihu_js_parser(lib):
    for line in lib:
        l = loads(line)
        yield  l['title']
        for j in l['answer']:
            yield j['answer']

def main():
    train( "review.txt", douban_review_parser)
    train( "zhihu.js", zhihu_js_parser)

if __name__ == "__main__":
    main()



