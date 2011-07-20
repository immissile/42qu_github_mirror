import _db
from _db import cursor_by_table
from oauth import oauth_token_by_oauth_id,\
OAUTH_GOOGLE, OAUTH_DOUBAN, \
OAUTH_SINA, OAUTH_TWITTER,\
OAUTH_WWW163, OAUTH_BUZZ,\
OAUTH_SOHU, OAUTH_QQ, \
OAUTH_RENREN,OAUTH_LINKEDIN 
from oauth_update import api_qq,api_douban, api_sina, api_www163, api_network_http, oauth_res_check



def api_douban_verify(key,secret,oauth_id):
    res = api_network_http( api_douban(
            '/people/@me',
            {},
            key,
            secret,
            "GET"
            ))
    if res.startswith('Signature does not match'):
        oauth_rm_by_oauth_id(oauth_id)
    else:
        return True


def api_sina_verify(key,secret):
    res = api_network_http( api_sina(
            "users/show.json",
            {},
            key,
            secret,
            "GET"
            ))
    

def api_qq_verify(key,secret):
    return api_qq(
            "/api/statuses/broadcast_timeline",
            {},
            key,
            secret,
            "GET",
            )

def api_www163_verify(key,secret):
    return api_www163(
            '/users/show.json',
            {},
            key,
            secret,
            "GET",
            )

DICT_API_VERIFY = {
        OAUTH_DOUBAN:api_douban_verify,
        OAUTH_SINA:api_sina_verify,
        OAUTH_WWW163:api_www163_verify,
        OAUTH_QQ:api_qq_verify
        }


def oauth_verify_by_oauth_id(oauth_id):
    out = oauth_token_by_oauth_id(oauth_id)
    if out:
        cid = out[0]
        if cid not in DICT_API_VERIFY.keys():
            return
        re = DICT_API_VERIFY[out[0]](out[1],out[2])
        mes = api_network_http(*re)
        print mes
        oauth_res_check(mes, oauth_id)


if __name__ == "__main__":
    oauth_verify_by_oauth_id(6)

