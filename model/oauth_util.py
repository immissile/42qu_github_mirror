#coding:utf-8
import uuid
import time
import base64
import binascii
import hashlib
import hmac
import urllib
import urlparse

def _oauth_escape(val):
    if isinstance(val, unicode):
        val = val.encode('utf-8')
    return urllib.quote(val, safe='~')

def _oauth10a_signature(consumer_token_secret, method, url, data=None, parameters={}, access_token_secret=None):
    """Calculates the HMAC-SHA1 OAuth 1.0a signature for the given request.

    See http://oauth.net/core/1.0a/#signing_process
    """
    parts = urlparse.urlparse(url)
    scheme, netloc, path = parts[:3]
    normalized_url = scheme.lower() + '://' + netloc.lower() + path

    base_elems = []
    base_elems.append(method.upper())
    base_elems.append(normalized_url)
    base_elems.append('&'.join('%s=%s' % (k, _oauth_escape(str(v)))
                               for k, v in parameters))

    base_string = '&'.join(_oauth_escape(e) for e in base_elems)
    key_elems = [_oauth_escape(consumer_token_secret)]
    key_elems.append(_oauth_escape(access_token_secret) if access_token_secret else '')
    key = '&'.join(key_elems)

    hash = hmac.new(key, base_string, hashlib.sha1)
    b = binascii.b2a_base64(hash.digest())[:-1]
    # print "-----------"
    # print key
    # print base_string
    # print b
    # print "-----------"
    return b

def _oauth_signature(consumer_token_secret, method, url, data=None, parameters={}, access_token_secret=None):
    parts = urlparse.urlparse(url)
    scheme, netloc, path = parts[:3]
    normalized_url = scheme.lower() + '://' + netloc.lower() + path

    base_elems = []
    base_elems.append(method.upper())
    base_elems.append(normalized_url)
    query = []
    query.extend(
         '%s=%s' % (k, _oauth_escape(str(v)))
         for k, v in parameters
    )

    base_elems.append('&'.join(query))

    base_string = '&'.join(_oauth_escape(e) for e in base_elems)
    key_elems = [consumer_token_secret]


    key_elems.append(access_token_secret if access_token_secret else '')
    key = '&'.join(key_elems)
    hash = hmac.new(key, base_string, hashlib.sha1)
    d = binascii.b2a_base64(hash.digest())[:-1]

    #print key
    #print base_string
    #print d
    return d


def oauth_request_parameters(url, api_key, api_secret, access_token, access_token_secret, parameters={}, method='GET', data=None, signature=_oauth_signature):
    base_args = dict(
        oauth_consumer_key=api_key,
        oauth_token=access_token,
        oauth_signature_method='HMAC-SHA1',
        oauth_timestamp=str(int(time.time())),
        oauth_nonce=binascii.b2a_hex(uuid.uuid4().bytes),
        oauth_version='1.0',
    )
    args = {}
    args.update(base_args)
    args.update(parameters)
    sign = signature(
        api_secret, method, url, data,
        sorted(args.items()),
        access_token_secret
    )
    base_args['oauth_signature'] = sign
    return base_args

def oauth_url(url, api_key, api_secret, access_token, access_token_secret, parameters={}, method='GET', data=None):
    args = oauth_request_parameters(url, api_key, api_secret, access_token, access_token_secret, parameters, method, data)
    return ''.join((url, '?', urllib.urlencode(args)))

def oauth10a_url(url, api_key, api_secret, access_token, access_token_secret, parameters={}, method='GET', data=None):
    args = oauth_request_parameters(url, api_key, api_secret, access_token, access_token_secret, parameters, method, data, _oauth10a_signature)
    return ''.join((url, '?', urllib.urlencode(args)))

def oauth_header(args, realm=''):
    auth_header = ['OAuth realm="%s"'%realm]
    # Add the oauth parameters.
    if args:
        for k, v in args.iteritems():
            if k[:6] == 'oauth_':
                auth_header.append(', %s="%s"' % (k, _oauth_escape(str(v))))
    return {'Authorization': ''.join(auth_header)}

if __name__ == '__main__':
    url = 'http://api.t.sina.com.cn/statuses/update.json'
    print oauth10a_url(
     url,
     'GDdmIQH6jhtmLUypg82g',
     'MCD8BKwGdgPHvAuvgvz4EQpqDAtx89grbuNMRd7Eh98',
     '819797-Jxq8aYUDRmykzVKrgoLhXSq67TEa5ruc4GJC2rWimw',
     'J6zix3FfA9LofH0awS24M3HcBYXO5nI1iYe8EfBA',
     parameters={
         'status':'通过OAuth发送微博信息'
     },
     method='POST'
    )
