#coding:utf-8
import urllib2, time, urllib, cookielib
from urllib import urlencode
from json import loads
from gauth import build_opener
from urlparse import unquote
from urllib import quote
from datetime import datetime
GOOGLE_URL_PREFIX = (
"http://www.google.com/reader/shared/",
"http://www.google.com/reader/public/atom/",
"https://www.google.com/reader/shared/",
"https://www.google.com/reader/public/atom/",

)
GV_LOGIN_URL = "https://www.google.com/accounts/ServiceLoginAuth"

def google_url_parse(url):
    for prefix in GOOGLE_URL_PREFIX:
        if url.startswith(prefix):
            url = url[len(prefix):]
            return unquote(url)
    return url

def feed_url(feed):
    feed = google_url_parse(feed)
    if not (feed.startswith("feed/") or feed.startswith("user/")):
        feed = "feed/"+feed
    return feed

def quote_feed_url(feed):
    feed = google_url_parse(feed)
    if feed.startswith("feed/"):
        feed = "feed/"+urllib.quote(feed[5:])
    elif not feed.startswith("user/"):
        feed = "feed/"+urllib.quote(feed)
    return feed

class Reader(object):
    def __init__(self, username, password):
        self.login(username, password)
        self.update_time = datetime(1990, 1, 1)

    def login(self, username, password):
        self.username = username
        self.password = password


        self.opener = build_opener(username, password)
        # authreq_data = urllib.urlencode({
        #     "Email": username,
        #     "Passwd": password,
        #     "service": "reader",
        #     "accountType": "GOOGLE",
        # })

        # auth_req = urllib2.Request('https://www.google.com/accounts/ClientLogin', data=authreq_data)
        # try:
        #     auth_resp = urllib2.urlopen(auth_req, timeout=20)
        # except urllib2.HTTPError, e:
        #     if e.code == 403:
        #         print "用户名或密码错误"
        #         return
        # auth_resp_body = auth_resp.read()

        # auth_resp_dict = dict(x.split("=", 1) for x in auth_resp_body.split("\n") if x)

        # print auth_resp_dict
        # auth = auth_resp_dict["Auth"].strip()

        # sid = auth_resp_dict["SID"].strip()

        # self.sid = sid
        self.get_token()
        self.ts = str(int(1000*time.time()))

    def get_token(self):

        r = urllib2.Request("https://www.google.com/reader/api/0/token")#, headers=headers)

        token = self.opener.open(r, timeout=20).read()
        #headers = {'Cookie': 'SID=%s; T=%s'%(sid, token)}
        #self.headers = headers
        self.token = token

    def get_url(self, url):
        #print url

        #r = urllib2.Request(url, headers=self.headers)
        #return urllib2.urlopen(r, timeout=20).read()
        #print url
        return self.opener.open(url, timeout=20).read()

    def get_json(self, url):
        content = self.get_url(url)
        content = content.replace("\t", " ")
        return loads(content)

    def single_feed(self, feed):
        feed = quote_feed_url(feed)
        return self.feed(feed)

    def feed(self, feed="user/-/state/com.google/reading-list?xt=user/-/state/com.google/read", n=100):
        c = None
        if feed.find("?") > 0:
            feed += "&"
        else:
            feed += "?"
        url_base = "https://www.google.com/reader/api/0/stream/contents/%sn=%s"%(feed, n)
        while True:
            url = url_base
            if c:
                url += "&c="+c
            data = self.get_json(url)
            if c is None and "updated" in data:
                self.update_time = datetime.fromtimestamp(int(data['updated']))

            c = data.get("continuation")
            for i in data.get("items"):
                yield i
            if c is None:
                break

    def post(self, url, token=True, data_string=None, **data ):
        #if token:
        #    self.get_token()
        count = 3
        while True:
            try:
                data.update({
                    "T":self.token
                })
                authreq_data = urllib.urlencode(data)
                if data_string:
                    authreq_data = "&".join((data_string, authreq_data))
                #print authreq_data
                auth_req = urllib2.Request(
                    url=url,
                    data=authreq_data,
                    #headers=self.headers
                )
                content = self.opener.open(auth_req, timeout=30).read()
            except urllib2.HTTPError, e:
                if count < 0:
                    raise
                else:
                    print "urllib2.HTTPError", e
                    count -= 1
                    self.login(self.username, self.password)
            else:
                return content

    def edit(self, action, target):
        url = "https://www.google.com/reader/api/0/subscription/edit?client=scroll"
        d = dict(
            ac=action, t=""
        )
        if type(target) is list:
            if target:
                d['data_string'] = "&".join(["s=%s"%i for i in map(quote, target)])
            else:
                return
        else:
            d['s'] = target
        return self.post(url, **d)

    def unsubscribe(self, feed):
        self.edit("unsubscribe", feed)

    def mark_as_read(self, feed="user/-/state/com.google/reading-list", ts=None):
        if ts is None:
            ts = self.ts+"999"
        url = "https://www.google.com/reader/api/0/mark-all-as-read?client=scroll"
        feed = feed_url(feed)
        return self.post(url, t="", s=feed, ts=ts)

    def subscription_list(self):
        subscription_list = self.get_json("https://www.google.com/reader/api/0/subscription/list?output=json")
        subscriptions = subscription_list.get("subscriptions")
        subscriptions = [i.get('id').encode("utf-8", "ignore") for i in subscriptions]
        return subscriptions

    def empty_subscription_list(self):
        subscription_list = self.subscription_list()
        #print len(subscription_list)
        while True:
            r = []
            while subscription_list:
                r.append(subscription_list.pop())
                if len(r) > 100:
                    break

            if not r:
                break
            else:
                self.unsubscribe(r)

    def subscribe(self, feed):
        return loads(self.post("https://www.google.com/reader/api/0/subscription/quickadd", quickadd=feed)).get("streamId")

    def info(self, feed):
        url = quote_feed_url(feed)
        url = "https://www.google.com/reader/api/0/stream/details?s=%s&fetchTrends=false&output=json"%url
        return self.get_json(url)

    def unread_feed(self):
        url = "https://www.google.com/reader/api/0/unread-count?output=json"
        result = self.get_json(url)
        r = []
        for i in result.get("unreadcounts", {}):
            id = i.get('id')
            if id:
                r.append(id)
        return r

    def unread(self, feed):
        url = "%s?xt=user/-/state/com.google/read"%quote(feed)
        return self.feed(url)








