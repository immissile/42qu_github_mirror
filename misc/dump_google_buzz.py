import urllib2
from urllib2 import urlopen as _urlopen
import traceback
import sys
import time
from time import sleep
from yajl import loads

def retry(func):
    def _(*args, **kwargs):
        tries = 2
        while tries:
            try:
                return func(*args, **kwargs)
            except urllib2.HTTPError, e:
                if e.getcode() == 404:
                    return
            except :
                time.sleep(0.1)
                tries -= 1
                sys.stdout.flush()
                traceback.print_exc()
        return func(*args, **kwargs)
    return _

URL = 'https://www.googleapis.com/buzz/v1/activities/%s/@public?alt=json&max-result=100'
#TODO YOUR KEY
key = '&key='

URL = URL+key

@retry
def urlopen(url):
    sys.stdout.flush()
    url = url.replace('&max-results=20', '&max-results=100')
    if '&key' not in url:
        url += key
    print url
    return _urlopen(url, timeout=60).read()


import Queue
import threading
import urllib2
import time
input = open('1.txt')
output = open('buzz.txt', 'w')



class Write(threading.Thread):
    def __init__(self, queue, write_queue):
        threading.Thread.__init__(self)
        self.write_queue = write_queue
        self.queue = queue

    def run(self):
        while True:
            line = self.write_queue.get()
            if line:
                output.write(line+'\n')
                output.flush()
                data = loads(line)
                links = data['data']['links']
                if 'next' in links:
                    nextlink = links['next'][0]['href']
                    self.queue.put(nextlink)
            while queue.qsize() < THREAD_NUM*2:
                for id in input:
                    self.queue.put(URL%id.strip())
                    break

            self.write_queue.task_done()

class ThreadUrl(threading.Thread):
    def __init__(self, queue, write_queue):
        threading.Thread.__init__(self)
        self.write_queue = write_queue
        self.queue = queue

    def run(self):
        while True:
            url = self.queue.get()
            sys.stdout.flush()
            result = urlopen(url)
            self.write_queue.put(result)
            self.queue.task_done()


queue = Queue.Queue()
write_queue = Queue.Queue()

THREAD_NUM = 20

def main():
    t = Write(queue, write_queue)
    t.setDaemon(True)
    t.start()
    for i in range(THREAD_NUM):
        t = ThreadUrl(queue, write_queue)
        t.setDaemon(True)
        t.start()


    for id in input:
        id = id.strip()
        queue.put(URL%id)
        if queue.qsize() > THREAD_NUM:
            break

    queue.join()
    write_queue.join()

main()
print 'dump'
sys.stdout.flush()
sleep(60)
output.close()
