import _db
import json
from _db import cursor_by_table
from oauth import oauth_token_by_oauth_id,\
OAUTH_GOOGLE, OAUTH_DOUBAN,\
OAUTH_SINA, OAUTH_TWITTER,\
OAUTH_WWW163,\
OAUTH_SOHU, OAUTH_QQ,\
OAUTH_RENREN, OAUTH_LINKEDIN
from oauth_update import api_qq, api_douban, api_sina, api_www163, api_renren, api_network_http
from config import SINA_FOLLOW
from oauth import oauth_rm_by_oauth_id



def api_douban_verify(key, secret, oauth_id):
    res = api_network_http(*api_douban(
            '/people/@me',
            {},
            key,
            secret,
            'GET'
            ))
    if res.startswith('Signature does not match'):
        oauth_rm_by_oauth_id(oauth_id)
    else:
        return True


def api_sina_verify(key, secret, oauth_id):
    res = api_network_http(*api_sina(
            '/users/show.json',
            {'user_id':SINA_FOLLOW},
            key,
            secret,
            'GET'
            ))
    if json.loads(res):
        m = json.loads(res)
        if int(m.get('error_code', '0')) == 401:
            oauth_rm_by_oauth_id(oauth_id)
        else:
            return True


def api_qq_verify(key, secret, oauth_id):
    res = api_network_http(*api_qq(
            '/api/user/info',
            {},
            key,
            secret,
            'GET',
            ))
    if json.loads(res):
        m = json.loads(res)
        if int(m.get('errcode', '0')) == 9:
            oauth_rm_by_oauth_id(oauth_id)
        else:
            return True

def api_www163_verify(key, secret, oauth_id):
    res = api_network_http(*api_www163(
            '/users/show.json',
            {},
            key,
            secret,
            'GET',
            ))
    if json.loads(res):
        m = json.loads(res)
        if int(m.get('error_code', '0')) == 401:
            oauth_rm_by_oauth_id(oauth_id)
        else:
            return True

def api_renren_verify(key, secret, oauth_id):
    res = api_network_http(*api_renren(
        key,
        secret,
        {'method':'users.getInfo'}
        ))
    if json.loads(res):
        m = json.loads(res)
        if isinstance(m,dict) and m.get('error_code'):
            oauth_rm_by_oauth_id(oauth_id)
        else:
            return True


DICT_API_VERIFY = {
        OAUTH_DOUBAN:api_douban_verify,
        OAUTH_SINA:api_sina_verify,
        OAUTH_WWW163:api_www163_verify,
        OAUTH_QQ:api_qq_verify,
        OAUTH_RENREN:api_renren_verify
        }


def oauth_verify_by_oauth_id(oauth_id):
    out = oauth_token_by_oauth_id(oauth_id)
    if out:
        cid, key, secret = out.cid, out.key, out.secret
        if cid not in DICT_API_VERIFY:
            return
        re = DICT_API_VERIFY[cid](key, secret, oauth_id)
        return re


if __name__ == '__main__':
    oauth_verify_by_oauth_id(31)

