#coding:utf-8
import _env
from idf import Idf
from config import ZDATA_PATH
from os.path import join

ZDATA_PATH_TRAIN_IDF = join(ZDATA_PATH,"train/idf") 

def train(filename, parser):
    idf = Idf()
    path = join(ZDATA_PATH_TRAIN_IDF, filename)
    with open(path) as f:
        for txt in parser(f):
            idf.append(txt)
    
    idf.tofile("%s.idf"%path)

def douban_review_parser(review):
    result = []

    for line in review:
        line = line.strip()
        if not line:
            continue
        if line.startswith(">->->"):
            if result:
                line = line.split(" ",5)
                result.append(line[-1])
                txt = "\n".join(result)
                yield txt
            result = []
        else:
            result.append(line)

def main():
    train( "review.txt", douban_review_parser)

if __name__ == "__main__":
    main() 



