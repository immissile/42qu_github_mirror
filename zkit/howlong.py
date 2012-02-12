#coding:utf-8

from time import time

class HowLong(object):
    def __init__(self, remain):
        self._begin = None
        self.done = 0
        self.remain = remain
 
    def remain_after_this(self):
        self.done += 1
        self.remain -= 1
        if self.done:
            if  self._begin is None:
                self._begin = time()
            diff = time() - self.begin
            sec = self.remain * diff / self.done
            return sec/3600.0 
    

if __name__ == "__main__":
    pass
    



