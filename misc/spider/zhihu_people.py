#coding:utf-8
from glob import glob

filelist = glob("/tmp/www.zhihu.com/*")
for i in filelist:
    with open(i) as f:
        for line in f:
            print line

if __name__ == "__main__":
    pass



