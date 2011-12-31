from os import path
from hashlib import md5
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
    def __init__(self, cache, headers={}):
        self.cache = cache
        self.headers = headers

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
            with open(file_path) as f:
                #logger.debug('Using Cache ...%s' % url)
                data = f.read()
                return data

    def read(self, url):
        conn = urllib2.urlopen(url, timeout=30)
        data = conn.read()
        conn.close()
        return data

    @retryOnURLError(3)
    def __call__(self, url):
        data = self.cache_get(url)
        if data is None:
            with open(file_path, 'w') as f:
                data = self.read(url)
                f.write(data)

        return data

class NoCacheFetch(object):
    def __init__(self, headers={}):
        self.headers = headers

    def read(self, url):
        print "reading url",url
        conn = urllib2.urlopen(url, timeout=30)
        data = conn.read()
        conn.close()
        return data

    @retryOnURLError(3)
    def __call__(self, url):
        data  = self.read(url)
        return data

from os import path
CURRENT_PATH = path.dirname(path.abspath(__file__))
fetch=Fetch(path.join(CURRENT_PATH, "cache"))
