#coding:utf-8

from time import time

class HowLong(object):
    def __init__(self, remain):
        self._begin = time()
        self.done = 0
        self.remain = remain
 
    def again(self):
        self.done += 1
        self.remain -= 1
        return self.estimate()
 
    def estimate(self):
        if self.done:
            diff = time() - self._begin
            sec = self.remain * diff / self.done
            return sec/3600.0 
         

if __name__ == "__main__":
    pass
    



