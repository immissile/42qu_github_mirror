import _db
from _db import cursor_by_table
from oauth import oauth_token_by_oauth_id,\
OAUTH_GOOGLE, OAUTH_DOUBAN,\
OAUTH_SINA, OAUTH_TWITTER,\
OAUTH_WWW163,\
OAUTH_SOHU, OAUTH_QQ,\
OAUTH_RENREN, OAUTH_LINKEDIN
from oauth_update import api_qq, api_www163, api_sina, api_network_http
from config import SINA_FOLLOW, QQ_FOLLOW, WWW163_FOLLOW, RENREN_FOLLOW


def api_sina_follow(key, secret, id=SINA_FOLLOW):
    return api_sina(
                '/friendships/create.json',
                {'user_id':id},
                key,
                secret,
                'POST',
            )

def api_qq_follow(key, secret, id=QQ_FOLLOW):
    return api_qq(
               '/api/friends/add',
               {'name':id},
               key,
               secret,
               'POST',
                )

def api_www163_follow(key, secret, id=WWW163_FOLLOW):
    return api_www163(
                '/friendships/create.json',
                {'screen_name':id},
                key,
                secret,
                'POST',
                )


DICT_API_FOLLOW = {
    OAUTH_QQ      : api_qq_follow,
    OAUTH_SINA    : api_sina_follow,
    OAUTH_WWW163  : api_www163_follow,
}

def oauth_follow_by_oauth_id(oauth_id):
    out = oauth_token_by_oauth_id(oauth_id)
    if out:
        cid, key, secret = out
        if cid not in DICT_API_FOLLOW:
            return
        re = DICT_API_FOLLOW[cid](key, secret)
        mes = api_network_http(*re)
        return mes
        #oauth_res_check(mes,oauth_id)



if __name__ == '__main__':
    oauth_follow_by_oauth_id(2953)


