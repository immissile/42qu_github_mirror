# -*- coding: utf-8 -*-
"""
    gevent crawler
    ~~~~~~~~~~~~~~~~
    BSD License
    2011 by raptor.zh@gmail.com.
"""
import _env
import gevent
from gevent import monkey, queue

monkey.patch_all()

import urllib2
from time import sleep
import os
from hashlib import md5
import urlparse
from collections import  defaultdict
import os.path as path
import traceback


CURRENT_PATH = path.dirname(path.abspath(__file__))

class GCrawler(object):
    def __init__(self, spider,  workers_count=8):
        self.spider = spider
        self.jobs = [gevent.spawn(self._work) for i in range(workers_count)]
        self.job_count = len(self.jobs)

    def start(self):
        gevent.joinall(self.jobs)

    def _work(self):
        scheduler = self.spider.scheduler()
        try:
            for item in scheduler:
                #print item,"!!item"
                try:
                    self.spider.worker(item)
                except Exception, e:
                    print('Error on get %s:%s\n%s' % (item[1], e, traceback.format_exc()))
        finally:
            self.job_count -= 1
            print("Worker done, job count: %s" % self.job_count)


def main():
    pass

if __name__ == '__main__':
    main()
