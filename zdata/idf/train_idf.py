#coding:utf-8
import _env
from df import Df
from config import ZDATA_PATH
from os.path import join,exists
from glob import glob
from idf import idf_dumps

ZDATA_PATH_TRAIN_IDF = join(ZDATA_PATH, "train/df")

def main():
    df = Df()

    def merge(filename):
        path = join(ZDATA_PATH_TRAIN_IDF, "%s.idf"%filename)

        if not exists(path):
            return

        df.extend_by_file(path)

    merge( "zhihu.js")
    merge( "review.txt")
    for i in glob(join(ZDATA_PATH_TRAIN_IDF, "wanfang", "Periodical_*")):
        merge(i)

    idf_dumps(join(ZDATA_PATH,"idf"), df._count, df._df)

if __name__ == "__main__":
    main()



