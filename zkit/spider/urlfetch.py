from os import path
import os
from hashlib import md5
import  time
import urllib2
import urlparse

def retryOnURLError(self, trycnt=3):
    def funcwrapper(fn):
        def wrapper( *args, **kwargs):
            for i in range(trycnt):
                try:
                    return fn( *args, **kwargs)
                except urllib2.URLError, e:
                    #logger.info('retry %s time(s)' % (i+1))
                    if i == trycnt - 1:
                        raise e
        return wrapper
    return funcwrapper

class Fetch(object):
    def __init__(self, cache, headers={}, sleep=0):
        self.cache = cache
        self.headers = headers
        self.sleep = sleep 

    def cache_get(self, url):
        cache_dir = path.join(
            self.cache, urlparse.urlparse(url).hostname
        )
        if not path.exists(cache_dir):
            os.mkdir(cache_dir)

        if not path.exists(cache_dir):
            os.mkdir(cache_dir)
        file_name = md5(url).hexdigest()
        file_path = path.join(cache_dir, file_name)

        if path.exists(file_path):
            print 'Using cache'
            with open(file_path) as f:
                data = f.read()
                return data

    def read(self, url):
        data = urlfetch(url, self.headers)
        if self.sleep:
            time.sleep(self.sleep)
        return data

    @retryOnURLError(3)
    def __call__(self, url):
        data = self.cache_get(url)
        if data is None:
            cache_dir = path.join(
                    self.cache, urlparse.urlparse(url).hostname
                    )
            file_name = md5(url).hexdigest()
            file_path = path.join(cache_dir, file_name)
            with open(file_path, 'w') as f:
                data = self.read(url)
                f.write(data)

        return data

def urlfetch(url, headers={}):
    request = urllib2.Request(
        url=url,
        headers=headers
    )

    urlopener = urllib2.build_opener()
    r = urlopener.open(request, timeout=30)
    j = r.read()

    return j

class MultiHeadersFetch(object):
    def __init__(self,  headers=() ):
        self._headers = headers
        self.pos = 0

    @property
    def headers(self):
        _headers = self._headers
        
        self.pos = (self.pos+1)%len(_headers) 
        while True:
            return _headers[self.pos]
    
    def read(self, url):
        headers = self.headers
        #print headers
        data = urlfetch(url, headers)
        return data

    @retryOnURLError(3)
    def __call__(self, url):
        data = self.read(url)
        return data

class NoCacheFetch(object):
    def __init__(self, sleep=0, headers={} ):
        self.headers = headers
        self.sleep = sleep

    def read(self, url):
        data = urlfetch(url, self.headers)
        if self.sleep:
            time.sleep(self.sleep)
        return data

    @retryOnURLError(3)
    def __call__(self, url):
        data = self.read(url)
        return data



from os import path
CURRENT_PATH = path.dirname(path.abspath(__file__))
fetch = Fetch(path.join(CURRENT_PATH, 'cache'))
