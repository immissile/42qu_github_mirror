#coding:utf-8
#coding:utf-8
import urllib2, time, urllib
from yajl import loads
from urlparse import unquote
from urllib import quote
from urllib2 import HTTPError, URLError


GOOGLE_URL_PREFIX = (
'http://www.google.com/reader/shared/',
'http://www.google.com/reader/public/atom/',
'https://www.google.com/reader/shared/',
'https://www.google.com/reader/public/atom/',
)

def google_url_parse(url):
    for prefix in GOOGLE_URL_PREFIX:
        if url.startswith(prefix):
            url = url[len(prefix):]
            return unquote(url)
    return url

def feed_url(feed):
    feed = google_url_parse(feed)
    if not (feed.startswith('feed/') or feed.startswith('user/')):
        feed = 'feed/'+feed
    return feed

def quote_feed_url(feed):
    feed = google_url_parse(feed)
    if feed.startswith('feed/'):
        feed = 'feed/'+urllib.quote(feed[5:])
    elif not feed.startswith('user/'):
        feed = 'feed/'+urllib.quote(feed)
    return feed

class Reader(object):
    def __init__(self, username, password):
        self.login(username, password)

    def login(self, username, password):
        self.username = username
        self.password = password
        authreq_data = urllib.urlencode({
            'Email': username,
            'Passwd': password,
            'service': 'reader',
            'accountType': 'GOOGLE',
        })

        auth_req = urllib2.Request('https://www.google.com/accounts/ClientLogin', data=authreq_data)
        try:
            auth_resp = urllib2.urlopen(auth_req, timeout=20)
        except urllib2.HTTPError, e:
            if e.code == 403:
                print '用户名或密码错误'
                return
        auth_resp_body = auth_resp.read()
        auth_resp_dict = dict(x.split('=', 1) for x in auth_resp_body.split('\n') if x)

        auth = auth_resp_dict['Auth'].strip()

        #sid = auth_resp_dict["SID"].strip()
        #lsid = auth_resp_dict["LSID"].strip()
        self.auth = auth
        #self.lsid = lsid
        #self.sid = sid
        self.get_token()
        self.ts = str(int(1000*time.time()))

    def get_token(self):
        #sid = self.sid
        #headers = {'Cookie': 'SID=%s; LSID=%s; Auth=%s;'%(sid, self.lsid, self.auth)}
        headers = {}
        headers['Authorization'] = 'GoogleLogin auth=' + self.auth
        r = urllib2.Request('https://www.google.com/reader/api/0/token', headers=headers)

        token = urllib2.urlopen(r, timeout=40).read()
        #headers = {'Cookie': 'SID=%s; T=%s'%(sid, token)}
        self.headers = headers
        self.token = token

    def get_url(self, url):
        #print url
        try:
            r = urllib2.Request(url, headers=self.headers)
            return urllib2.urlopen(r, timeout=40).read()
        except (HTTPError, URLError):
            print url

    def get_json(self, url):
        content = self.get_url(url)
        content = content.replace('\t', ' ')
        return loads(content)

    def single_feed(self, feed):
        feed = quote_feed_url(feed)
        return self.feed(feed)

    def feed(self, feed='user/-/state/com.google/reading-list?xt=user/-/state/com.google/read'):
        c = None
        if feed.find('?') > 0:
            feed += '&'
        else:
            feed += '?'
        url_base = 'https://www.google.com/reader/api/0/stream/contents/%sn=100'%feed
        while True:
            url = url_base
            if c:
                url += '&c='+c
            data = self.get_json(url)
            c = data.get('continuation')
            for i in data.get('items'):
                yield i
            if c is None:
                break

    def post(self, url, token=True, **data):
        #if token:
        #    self.get_token()
        count = 3
        while True:
            try:
                data.update({
                    'T':self.token
                })
                authreq_data = urllib.urlencode(data)
                auth_req = urllib2.Request(
                    url=url,
                    data=authreq_data,
                    headers=self.headers
                )
                content = urllib2.urlopen(auth_req, timeout=20).read()
            except urllib2.HTTPError, e:
                if count < 0:
                    raise
                else:
                    print 'urllib2.HTTPError', e
                    count -= 1
                    self.login(self.username, self.password)
            else:
                return content

    def edit(self, action, target):
        url = 'https://www.google.com/reader/api/0/subscription/edit?client=scroll'
        return self.post(url, ac=action, s=target, t='')

    def unsubscribe(self, feed):
        self.edit('unsubscribe', feed)

    def mark_as_read(self, feed='user/-/state/com.google/reading-list', ts=None):
        if ts is None:
            ts = self.ts+'999'
        url = 'https://www.google.com/reader/api/0/mark-all-as-read?client=scroll'
        feed = feed_url(feed)
        return self.post(url, t='', s=feed, ts=ts)

    def subscription_list(self):
        subscription_list = self.get_json('https://www.google.com/reader/api/0/subscription/list?output=json')
        subscriptions = subscription_list.get('subscriptions')
        subscriptions = [i.get('id').encode('utf-8', 'ignore') for i in subscriptions]
        return subscriptions

    def empty_subscription_list(self):
        for i in self.subscription_list():
            self.unsubscribe(i)

    def subscribe(self, feed):
        return loads(self.post('https://www.google.com/reader/api/0/subscription/quickadd', quickadd=feed)).get('streamId')

    def info(self, feed):
        url = quote_feed_url(feed)
        url = 'https://www.google.com/reader/api/0/stream/details?s=%s&fetchTrends=false&output=json'%url
        return self.get_json(url)

    def unread_feed(self):
        url = 'https://www.google.com/reader/api/0/unread-count?output=json'
        result = self.get_json(url)
        r = []
        for i in result.get('unreadcounts', {}):
            id = i.get('id')
            if id:
                r.append(id)
        return r

    def unread(self, feed):
        feed = quote_feed_url(feed)
        url = '%s?xt=user/-/state/com.google/read'%feed
        return self.feed(url)

    def subscription_item_dump(self):
        for subscription in self.subscription_list():
            if not subscription.startswith('feed/'):
                continue
            if '?' in subscription:
                q_subscription = quote(subscription)
            try:
                for i in self.feed(q_subscription):
                    yield subscription, i
            except HTTPError, e:
                if e.code == 404:
                    print subscription
                    continue





