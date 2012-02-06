#coding:utf-8
import _env
import mmseg
from os.path import abspath, dirname, join


filepath = join(dirname(abspath(mmseg.__file__)), 'data/chars.dic')
def chariter():
    with open(filepath) as charline:
        for i in charline:
            i = i.strip().split()
            if len(i) == 2:
                yield i[-1]

if __name__ == '__main__':
    pass



