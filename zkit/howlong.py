#coding:utf-8

from time import time

class HowLong(object):
    def __init__(self, remain):
        self._begin = time()
        self._done = 0
        self._remain = remain
 
    def done(self):
        self._done += 1
        self._remain -= 1
        if self._done: 
            diff = time() - self._begin
            sec = self._remain * diff / self._done
            return sec/3600.0 
    

if __name__ == "__main__":
    pass
    



