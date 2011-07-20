import _db
from _db import cursor_by_table
from oauth import oauth_token_by_oauth_id,\
OAUTH_GOOGLE, OAUTH_DOUBAN, \
OAUTH_SINA, OAUTH_TWITTER,\
OAUTH_WWW163, OAUTH_BUZZ,\
OAUTH_SOHU, OAUTH_QQ, \
OAUTH_RENREN,OAUTH_LINKEDIN 
from oauth_update import api_qq,api_www163,api_sina, api_network_http, oauth_res_check


def api_sina_follow(key,secret,id='1827906323'):
    print 'sina'
    print api_sina(
                "/friendships/create.json",
                {'user_id':id},
                key,
                secret,
                'POST',
            )


    return api_sina(
                "/friendships/create.json",
                {'user_id':id},
                key,
                secret,
                'POST',
            )

def api_qq_follow(key,secret,id='cn42qu'):
    print 'qq'
    print api_qq(
               '/api/friends/addspecial',
               {'name':id},
               key,
               secret,
               'POST',
                )


    return api_qq(
               '/api/friends/add',
               {'name':id},
               key,
               secret,
               'POST',
                )

def api_www163_follow(key,secret,id='6122584690'):
    print 'www163'
    print api_www163(
                '/friendships/create.json',
                {'screen_name':id},
                key,
                secret,
                'POST',
                )


    return api_www163(
                '/friendships/create.json',
                {'screen_name':id},
                key,
                secret,
                'POST',
                )


DICT_API_FOLLOW = {
        OAUTH_QQ:api_qq_follow,
        OAUTH_SINA:api_sina_follow,
        OAUTH_WWW163:api_www163_follow,
    }

def oauth_follow_by_oauth_id(oauth_id):
    out = oauth_token_by_oauth_id(oauth_id)
    if out:
        cid = out[0]
        if cid not in DICT_API_FOLLOW.keys():
            return
        re = DICT_API_FOLLOW[out[0]](out[1],out[2])
        mes = api_network_http(*re)
        print mes
        #oauth_res_check(mes,oauth_id)



if __name__ == "__main__":
    oauth_follow_by_oauth_id(9)
    

