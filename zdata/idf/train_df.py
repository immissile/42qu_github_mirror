#coding:utf-8
import _env
from df import Df
from config import ZDATA_PATH
from os.path import join, exists
from yajl import loads
from glob import glob
from os import mkdir
#import envoy

ZDATA_PATH_TRAIN_IDF = join(ZDATA_PATH, "train/df")

def train(filename, parser):
    if filename.endswith(".idf"):
        return

    path = join(ZDATA_PATH_TRAIN_IDF, filename)

    tofile = "%s.idf"%path
    if exists(tofile):
        #cmd = 'scp %s work@stdyun.com:%s'%(tofile, tofile)
        #print cmd
        #r = envoy.run(cmd)
        #print r.std_out
        return

    if not exists(path):
        return

    df = Df()
    count = 0
    with open(path) as f:
        for txt in parser(f):
            df.append(txt)
            if count%1000 == 1:
                print filename, count
            count += 1

    df.tofile(tofile)

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

def wanfang_parser(stdin):
    for line in stdin:
        f = filter(bool, loads(line)[:2])
        yield "\n".join(f)


def main():
    pass
    train( "zhihu.js", zhihu_js_parser)
    train( "review.txt", douban_review_parser)
    for i in glob(join(ZDATA_PATH_TRAIN_IDF, "wanfang", "Periodical_*")):
        train(i, wanfang_parser)

if __name__ == "__main__":
    main()



