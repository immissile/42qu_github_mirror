#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading

class LockFile(file):
    def __init__(self, name , mode='r'):
        super(LockFile, self).__init__(name,mode)
        self.Rlock =  threading.RLock()

    def write(self,chunk):
        with self.Rlock:
            super(LockFile,self).write(chunk)
        

if __name__ == '__main__':
    newtest = LockFile('test','w')
    newtest.write("DDDD")
