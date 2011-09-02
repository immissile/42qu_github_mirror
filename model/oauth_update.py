#coding:utf-8
import urllib2
from urllib2 import urlopen, HTTPError
import urllib
from urllib import urlencode
import _db
import json
import traceback
import httplib
from zkit.txt import cnenoverflow
from xml.sax.saxutils import escape, quoteattr
from oauth_util import oauth_url, oauth_request_parameters, oauth_header, _oauth_escape
from shorturl import shorturl
from config import DOUBAN_CONSUMER_SECRET, DOUBAN_CONSUMER_KEY,\
SINA_CONSUMER_SECRET, SINA_CONSUMER_KEY,\
QQ_CONSUMER_SECRET, QQ_CONSUMER_KEY,\
TWITTER_CONSUMER_SECRET, TWITTER_CONSUMER_KEY,\
WWW163_CONSUMER_SECRET, WWW163_CONSUMER_KEY,\
GOOGLE_CONSUMER_SECRET
from oauth import oauth_token_by_oauth_id,\
OAUTH_GOOGLE, OAUTH_DOUBAN,\
OAUTH_SINA, OAUTH_TWITTER,\
OAUTH_WWW163, \
OAUTH_SOHU, OAUTH_QQ,\
OAUTH_RENREN, OAUTH_LINKEDIN

from collections import defaultdict
from oauth import oauth_rm_by_oauth_id

def api_xxx(
        api_key, api_secret,
        host, netloc, parameters, key, secret, method='POST', data=None, content_type='application/x-www-form-urlencoded', realm='',
    ):
    url = 'http://%s%s'%(host, netloc)
    post_param = oauth_request_parameters(
        url,
        api_key, api_secret,
        key,
        secret,
        method=method,
        parameters=parameters,
        data=data,
    )
    if method == 'POST':
        if data is None:
            body = urlencode(parameters)
        else:
            body = data
    else:
        body = ''
        netloc = url+'?'+urlencode(parameters)


    headers = oauth_header(post_param, realm)
    headers['Accept'] = 'text/html'
    headers['User-Agent'] = '42qu'
    headers['Content-Type'] = content_type
    return  host, netloc, headers, body, method


def api_url_param(
        api_key, api_secret,
        host, netloc, parameters, key, secret, method='POST', data=None, content_type='application/x-www-form-urlencoded', realm='',
    ):
    url = 'http://%s%s'%(host, netloc)
    post_param = oauth_request_parameters(
        url,
        api_key, api_secret,
        key,
        secret,
        method=method,
        parameters=parameters,
        data=data,
    )
    if data is None:
        body = urlencode(parameters)
    else:
        body = data
    headers = {}
    #oauth_header(post_param, realm)
    #headers["Accept"] = "text/html"
    #headers["User-Agent"] = "42qu"
    headers['Content-Type'] = content_type
    return  host, netloc+'?'+urlencode(post_param), headers, body, method


def api_buzz(netloc, parameters, key, secret, method='POST', data=None):
    host = 'www.googleapis.com'
    netloc = '/buzz/v1%s?key=%s&alt=json'%(netloc, BUZZ_KEY)
    api_key = DOMAIN
    api_secret = GOOGLE_CONSUMER_SECRET
    return api_xxx(api_key, api_secret,
        host,
        netloc,
        parameters,
        key,
        secret,
        method,
        data,
        'application/json',
    )

def api_www163(netloc, parameters, key, secret, method='POST'):
    host = 'api.t.163.com'
    api_key = WWW163_CONSUMER_KEY
    api_secret = WWW163_CONSUMER_SECRET
    return api_xxx(api_key, api_secret,
        host,
        netloc,
        parameters,
        key,
        secret,
        method
    )

def api_twitter(netloc, parameters, key, secret, method='POST'):
    host = 'api.twitter.com'
    api_key = TWITTER_CONSUMER_KEY
    api_secret = TWITTER_CONSUMER_SECRET
    return api_xxx(api_key, api_secret,
        host,
        '/1%s'%netloc,
        parameters,
        key,
        secret,
        method
    )

def api_qq(netloc, parameters, key, secret, method='POST'):
    host = 'open.t.qq.com'
    api_key = QQ_CONSUMER_KEY
    api_secret = QQ_CONSUMER_SECRET
    return api_url_param(api_key, api_secret,
        host,
        netloc,
        parameters,
        key,
        secret,
        method
    )

def api_sina(netloc, parameters, key, secret, method='POST'):
    host = 'api.t.sina.com.cn'
    api_key = SINA_CONSUMER_KEY
    api_secret = SINA_CONSUMER_SECRET
    return api_xxx(api_key, api_secret,
        host,
        netloc,
        parameters,
        key,
        secret,
        method
    )

def api_douban(netloc, parameters, key, secret, method='POST', data=None):
    host = 'api.douban.com'
    api_key = DOUBAN_CONSUMER_KEY
    api_secret = DOUBAN_CONSUMER_SECRET
    return api_xxx(api_key, api_secret,
        host,
        netloc,
        parameters,
        key,
        secret,
        method,
        data,
        'application/atom+xml'
    )


def api_twitter_say(key, secret, word):
    return
    #TODO
    return api_twitter(
        '/statuses/update.json',
        {'status':word},
        key,
        secret,
        'POST',
    )

def api_douban_say(key, secret, word):
    data = """<?xml version='1.0' encoding='UTF-8'?>
<entry xmlns:ns0="http://www.w3.org/2005/Atom" xmlns:db="http://www.douban.com/xmlns/">
<content>%s</content>
</entry>"""%escape(str(word))
    return api_douban(
        '/miniblog/saying',
        {},
        key,
        secret,
        'POST',
        data
    )

def api_qq_say(key, secret, word):
    r = api_qq(
        '/api/t/add',
        {'content':word},
        key,
        secret,
        'POST',
    )
    #print r
    return r

def api_sina_say(key, secret, word):
    return api_sina(
        '/statuses/update.json',
        {'status':word},
        key,
        secret,
        'POST',
    )

def api_buzz_say(key, secret, word):
    r = api_buzz(
        '/people/@me/@self',
        {},
        key,
        secret,
        'GET',
    )
    return r
    return api_buzz(
        '/activities/@me/@self',
        {},
        key,
        secret,
        'POST',
"""{
"data": {
"object": {
"type": "note",
"content": "test"
}
}
}""",
    )

def api_www163_say(key, secret, word):
    return api_www163(
        '/statuses/update.json',
        {
            'status':word
        },
        key,
        secret,
        'POST',
    )


DICT_API_SAY = {
        OAUTH_QQ:api_qq_say,
        OAUTH_SINA:api_sina_say,
        OAUTH_WWW163:api_www163_say,
        OAUTH_TWITTER:api_twitter_say,
        OAUTH_DOUBAN:api_douban_say
        }

def oauth_txt_cat(cid, txt, url):
    url_len = len(str(url))
    if cid == OAUTH_DOUBAN:
        txt = str(txt).decode('utf-8')
        tword = txt[:140-url_len]
        if tword != txt:
            txt = txt[:137-url_len]+'...'
        txt = str(txt)+url
        return txt
    else:
        txt = cnenoverflow(str(txt), 139-url_len)[0]+' '+url
        return txt


def sync_by_oauth_id(oauth_id, txt, url=None):
    out = oauth_token_by_oauth_id(oauth_id)
    if out:
        cid, key, secret = out
        #url = shorturl(url)
        txt = oauth_txt_cat(cid, txt, url)
        re = DICT_API_SAY[cid](key, secret, txt)
        if re:
            mes = api_network_http(*re)
            #oauth_res_check(mes, oauth_id)
            return mes

def api_network_http(host, netloc, headers, body, method, connection=httplib.HTTPConnection):
    conn = connection(host, timeout=30)
    #conn.set_debuglevel(1)
    conn.request(method, netloc, headers=headers, body=body)
    resp = conn.getresponse()
    r = resp.read()
    conn.close()
    #print r
    return r

if __name__ == '__main__':
    p = sync_by_oauth_id(3, '''42qu.com : 人来人往 , 这是我们相遇的地方关注42qu的官方微博
            我很牛逼哟''', 'http://42qu.com/zhendi')
