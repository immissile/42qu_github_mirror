import urllib2
from urllib2 import urlopen as _urlopen
import traceback
import sys
import time
from bsddb3 import hashopen
from time import sleep
from random import choice

db = hashopen("google.db")

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

URL = "https://www.googleapis.com/buzz/v1/people/%s/@self?alt=json&key=%s"
API_KEY = (
)

@retry
def urlopen(id):
    key = choice(API_KEY)

    url = URL%(id.strip(),key)
    return _urlopen(url, timeout=60).read()


import Queue
import threading
import urllib2
import time
input = open("1.txt")
output = open("data.txt","w")

class Write(threading.Thread):
    def __init__(self, queue, write_queue):
        threading.Thread.__init__(self)
        self.write_queue = write_queue
        self.queue = queue

    def run(self):
        while True:
            line = self.write_queue.get()
            for id in input:
                self.queue.put(id)
                break
            if line:
                output.write(line+"\n")
                output.flush()
            self.write_queue.task_done()

class ThreadUrl(threading.Thread):
    def __init__(self, queue, write_queue):
        threading.Thread.__init__(self)
        self.write_queue = write_queue
        self.queue = queue

    def run(self):
        while True:
            id = self.queue.get()
            id = id.strip()
            sys.stdout.flush()
            result = urlopen(id)
            if result:
                print id
                sys.stdout.flush()
            self.write_queue.put(result)
            self.queue.task_done()


queue = Queue.Queue()
write_queue = Queue.Queue()

THREAD_NUM = 20

def main():
    t = Write(queue,write_queue)
    t.setDaemon(True)
    t.start()
    for i in range(THREAD_NUM):
        t = ThreadUrl(queue,write_queue)
        t.setDaemon(True)
        t.start()


    for id in input:
        queue.put(id)
        if queue.qsize() > THREAD_NUM:
            break

    queue.join()
    write_queue.join()

main()
print "done"
sys.stdout.flush()
sleep(60)
output.close()
