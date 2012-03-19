#coding:utf-8
import sgmllib, urlparse, re, sys
import urllib, urllib2

API_KEY = 'ABQIAAAApDjU7EwhyOJaBrF_GABYnRTWDsCWafW7AFWlPKY2v-OqDNyoWBQpqdnJzqgW6ZK_WJKFfDpuoJNifw'

GOOGLE_RSS_TEMPLATE = 'https://www.google.com/reader/api/0/feed-finder?key=%s&output=json&q=%%s'%API_KEY

GOOGLE_AJAX_RSS = 'https://ajax.googleapis.com/ajax/services/feed/lookup?v=1.0&key=%s&q=%%s'%API_KEY

RSS_DETAIL = 'https://ajax.googleapis.com/ajax/services/feed/load?v=1.0&num=0&hl=zh-CN&q='

class URLGatekeeper:
    """a class to track robots.txt rules across multiple servers"""
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
           'Accept': ' text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
           'Accept-Language':'zh-cn,zh;q=0.5',
           'Accept-Charset':'gb18030,utf-8;q=0.7,*;q=0.7',
           'Content-type':'application/x-www-form-urlencoded'
        }

        self.urlopener = urllib2.build_opener()

    def get(self, url):
        r = urllib2.Request(url, headers=self.headers)
        try:
            return self.urlopener.open(r, timeout=10).read()
        except:
            return ''

_gatekeeper = URLGatekeeper()

class BaseParser(sgmllib.SGMLParser):
    def __init__(self, baseuri):
        sgmllib.SGMLParser.__init__(self)
        self.links = []
        self.baseuri = baseuri

    def normalize_attrs(self, attrs):
        def cleanattr(v):
            v = sgmllib.charref.sub(lambda m: unichr(int(m.groups()[0])), v)
            v = v.strip()
            v = v.replace('&lt;', '<').replace('&gt;', '>').replace('&apos;', "'").replace('&quot;', '"').replace('&amp;', '&')
            return v
        attrs = [(k.lower(), cleanattr(v)) for k, v in attrs]
        attrs = [(k, k in ('rel', 'type') and v.lower() or v) for k, v in attrs]
        return attrs

    def do_base(self, attrs):
        attrsD = dict(self.normalize_attrs(attrs))
        if not attrsD.has_key('href'): return
        self.baseuri = attrsD['href']

    def error(self, *a, **kw): pass # we're not picky

class LinkParser(BaseParser):
    FEED_TYPES = ('application/rss+xml',
                  'text/xml',
                  'application/atom+xml',
                  'application/x.atom+xml',
                  'application/x-atom+xml')
    def do_link(self, attrs):
        attrsD = dict(self.normalize_attrs(attrs))
        if not attrsD.has_key('rel'): return
        rels = attrsD['rel'].split()
        if 'alternate' not in rels: return
        if attrsD.get('type') not in self.FEED_TYPES: return
        if not attrsD.has_key('href'): return
        self.links.append(urlparse.urljoin(self.baseuri, attrsD['href']))

def makeFullURI(uri):
    uri = uri.strip()
    if uri.startswith('feed://'):
        uri = 'http://' + uri.split('feed://', 1).pop()
    for x in ['http', 'https']:
        if uri.startswith('%s://' % x):
            return uri
    return 'http://%s' % uri

def getLinks(data, baseuri):
    p = LinkParser(baseuri)
    p.feed(data)
    return p.links

r_brokenRedirect = re.compile('<newLocation[^>]*>(.*?)</newLocation>', re.S)
def tryBrokenRedirect(data):
    if '<newLocation' in data:
        newuris = r_brokenRedirect.findall(data)
        if newuris: return newuris[0].strip()

def couldBeFeedData(data):
    data = data.lower()
    if data.count('<html'): return 0
    return data.count('<rss') + data.count('<rdf') + data.count('<feed')


from yajl import loads
from traceback import print_exc
def feeds(uri, all=False, _recurs=None):
    if uri.startswith('https://www.google.com/reader/') or uri.startswith('http://www.google.com/reader/'):
        if uri.startswith('http://'):
            uri = 'https'+uri[4:]
        quri = uri
    else:
        quri = urllib.quote(uri)

    url = GOOGLE_AJAX_RSS%quri
    #print url
    try:
        body = urllib2.urlopen(url, timeout=30).read()
        body = loads(body)
    #    print body
    except:
        print_exc()
    else:
        if body.get('responseStatus') == 200:
            url = body['responseData']['url']
            if url:
                url = url.encode('utf-8', 'ignore')
                #print "!!",type(url)
                return [url]


    url = GOOGLE_RSS_TEMPLATE%quri
    try:
        #print url
        body = urllib2.urlopen(url, timeout=10).read()
        body = loads(body)
    except:
        print_exc()
    else:
        f = body.get('feed', [])
        if f:
            result = []
            for i in f:
                href = i.get('href')
                if href:
                    result.append(href)
            if result:
                return result

    if _recurs is None: _recurs = [uri]
    fulluri = makeFullURI(uri)
    data = _gatekeeper.get(fulluri)

    # is this already a feed?
    if couldBeFeedData(data):
        return [fulluri]

    newuri = tryBrokenRedirect(data)

    if newuri and newuri not in _recurs:
        _recurs.append(newuri)
        return feeds(newuri, all=all, _recurs=_recurs)

    try:
        outfeeds = getLinks(data, fulluri)
    except:
        outfeeds = []

    result = []
    for i in outfeeds:
        if i not in result:
            result.append(i)
    return result

def feed(uri):
    #todo: give preference to certain feed formats
    feedlist = feeds(uri)
    if feedlist:
        return feedlist[0]
    else:
        return None

from urllib2 import urlopen
from urllib import quote
from urlparse import unquote
import urllib2
import urllib
import traceback
from yajl import loads
import re



def get_rss_basic_json(url):
    if url.startswith('https://www.google.com/reader/') or url.startswith('http://www.google.com/reader/'):
        if url.startswith('http://'):
            url = 'https'+url[4:]
        url = unquote(url)

    detail_url = RSS_DETAIL+quote(url)
    try:
        r = urlopen(detail_url, timeout=10).read()
    except:
        traceback.print_exc()

    r = loads(r)
    if r['responseStatus'] == 200:
        return r

def parse_rss_baisc_json(r):
    feed = r['responseData']['feed']
    title = feed.get('title', '')
    link = feed.get('link', '')

    if title.startswith('Twitter / '):
        title = title[10:]+'说'
    title = title.replace("'s shared items in Google Reader", ' Google阅读器 共享条目')
    title = title.replace("'s starred items in Google Reader", ' Google阅读器 加星条目')
    description = feed.get('description', '')

    return feed['feedUrl'], link, title

def get_rss_link_title_by_rss(rss):
    r = get_rss_basic_json(rss)
    if r:
        return parse_rss_baisc_json(r)
    return None, None, None

def get_rss_link_title_by_url(url):
    rss_url = feed(url)
    if rss_url:
        return get_rss_link_title_by_rss(rss_url)
    return None, None, None

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    uri = 'http://zsp.javaeye.com'
    print feeds(uri)
    for i in get_rss_link_title_by_url(uri):
        print i

