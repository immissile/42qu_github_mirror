#coding:utf-8
from _db import cursor_by_table, McNum, Model

OAUTH_GOOGLE = 1
OAUTH_DOUBAN = 2
OAUTH_SINA = 3
OAUTH_TWITTER = 4
OAUTH_WWW163 = 5
OAUTH_BUZZ = 6
OAUTH_SOHU = 7
OAUTH_QQ = 8
OAUTH_RENREN = 9
OAUTH_LINKEDIN = 10

OAUTH2NAME_DICT = {
    OAUTH_GOOGLE    : 'Google'      ,
    OAUTH_WWW163    : '网易微博'    ,
    OAUTH_SOHU      : '搜狐微博'    ,
    OAUTH_QQ        : '腾讯微博'    ,
    OAUTH_RENREN    : '人人网'      ,
    OAUTH_DOUBAN    : '豆瓣'        ,
    OAUTH_SINA      : '新浪微博'    ,
    OAUTH_BUZZ      : 'Buzz'        ,
    OAUTH_TWITTER   : 'Twitter'     ,
    OAUTH_LINKEDIN  : 'LinkedIn'    ,
}

OAUTH_TUPLE = (
    OAUTH_DOUBAN    ,
    OAUTH_RENREN    ,
    OAUTH_SINA      ,
    OAUTH_QQ        ,
    OAUTH_WWW163    ,
    OAUTH_SOHU      ,
    OAUTH_TWITTER   ,
)


OAUTH2URL = {
    OAUTH_DOUBAN:'http://www.douban.com/people/%s/',
    OAUTH_SINA:'http://t.sina.com.cn/%s',
    OAUTH_TWITTER:'http://twitter.com/%s',
    OAUTH_WWW163:'http://t.163.com/%s',
    OAUTH_SOHU:'http://t.sohu.com/%s',
#    OAUTH_BUZZ:'%s',
    OAUTH_QQ:'http://t.qq.com/%s',
}

OAUTH2TABLE = {
    #OAUTH_BUZZ:"oauth_token_buzz",
    OAUTH_TWITTER:'oauth_token_twitter',
    OAUTH_SOHU:'oauth_token_sohu',
    OAUTH_SINA:'oauth_token_sina',
    OAUTH_DOUBAN:'oauth_token_douban',
    OAUTH_WWW163:'oauth_token_www163',
    OAUTH_QQ:'oauth_token_qq',
}


OAUTH_SYNC_CID = set(
    OAUTH2NAME_DICT.iterkeys()
)

OAUTH_SYNC_SQL = 'app_id in (%s)' % (','.join(map(str, OAUTH_SYNC_CID)))

OAUTH_SYNC_TXT = "42区 , 这是一个神奇的网站 , 速来围观 !"


class OauthToken(Model):
    pass

def _oauth_sync_sum(zsite_id):
    c = OauthToken.raw_sql('select count(1) from oauth_token where zsite_id=%%s and %s' % OAUTH_SYNC_SQL, zsite_id).fetchone()
    return c[0]

oauth_sync_sum = McNum(
    _oauth_sync_sum, 'OauthSyncSum=%s'
)

def name_uid_set( id, name, uid, table):
    cursor = OauthToken.raw_sql('select id from %s where id=%%s'%table, id)
    sql_tuple = (name, uid, id)
    if cursor.fetchone():
        OauthToken.raw_sql('update %s set name=%%s,uid=%%s where id=%%s'%table, *sql_tuple)
    else:
        OauthToken.raw_sql(
            'insert into %s (name,uid,id) values (%%s,%%s,%%s)'%table,
            *sql_tuple
        )

def oauth_token_by_oauth_id(oauth_id):
    s = OauthToken.raw_sql('select app_id, token_key, token_secret from oauth_token where id =%s', oauth_id).fetchone()
    return s


def oauth_rm_by_oauth_id(oauth_id):
    cursor = cursor_by_table('oauth_token')
    cursor_new = cursor_by_table('oauth_token_backup')
    cursor.execute('select id,app_id,zsite_id,token_key,token_secret from oauth_token where id=%s', oauth_id)
    item = cursor.fetchone()
    if item:
        cursor_new.execute('insert into oauth_token_backup (id,app_id,zsite_id,token_key,token_secret) values (%s,%s,%s,%s,%s)', item)
        cursor.execute('delete from oauth_token where id =%s', oauth_id)



def oauth_save(app_id, zsite_id, token_key, token_secret):
    cursor = OauthToken.raw_sql('select id from oauth_token where zsite_id=%s and app_id=%s', zsite_id, app_id)
    id = cursor.fetchone()
    id = id and id[0]

    if id:
        OauthToken.raw_sql('update oauth_token set token_key=%s , token_secret=%s where id=%s', token_key, token_secret, id)
    else:
        id = OauthToken.raw_sql(
            'insert into oauth_token (app_id,zsite_id,token_key,token_secret) values (%s,%s,%s,%s)',
            app_id, zsite_id, token_key, token_secret
        ).lastrowid
    if app_id in OAUTH_SYNC_CID:
        oauth_sync_sum.delete(zsite_id)
    return id


def oauth_save_google(zsite_id, token_key, token_secret):
    oauth_save(OAUTH_GOOGLE, zsite_id, token_key, token_secret)

def oauth_save_renren(zsite_id, token_key, token_secret):
    oauth_save(OAUTH_RENREN, zsite_id, token_key, token_secret)

def oauth_save_with_uid(app_id, zsite_id, token_key, token_secret, name, uid):
    id = oauth_save(app_id, zsite_id, token_key, token_secret)
    name_uid_set(id, name, uid, OAUTH2TABLE[app_id])
    from model.zsite_link import  link_cid_new
    link_cid_new(zsite_id, app_id, (OAUTH2URL[app_id])%uid)

#def oauth_save_buzz(zsite_id, token_key, token_secret, name, uid):
#    oauth_save_with_uid(OAUTH_BUZZ, zsite_id, token_key, token_secret, name, uid)

def oauth_save_twitter(zsite_id, token_key, token_secret, name, uid):
    oauth_save_with_uid(OAUTH_TWITTER, zsite_id, token_key, token_secret, name, uid)

def oauth_save_sohu(zsite_id, token_key, token_secret, name, uid):
    oauth_save_with_uid(OAUTH_SOHU, zsite_id, token_key, token_secret, name, uid)

def oauth_save_qq(zsite_id, token_key, token_secret, name, uid):
    oauth_save_with_uid(OAUTH_QQ, zsite_id, token_key, token_secret, name, uid)

def oauth_save_sina(zsite_id, token_key, token_secret, name, uid):
    oauth_save_with_uid(OAUTH_SINA, zsite_id, token_key, token_secret, name, uid)

def oauth_save_douban(zsite_id, token_key, token_secret, name, uid):
    oauth_save_with_uid(OAUTH_DOUBAN, zsite_id, token_key, token_secret, name, uid)

def oauth_save_www163(zsite_id, token_key, token_secret, name, uid):
    oauth_save_with_uid(OAUTH_WWW163, zsite_id, token_key, token_secret, name, uid)

def oauth_by_zsite_id(zsite_id):
    cursor = OauthToken.raw_sql(
        'select app_id,id from oauth_token where zsite_id=%s', zsite_id
    )
    return cursor.fetchall()

def name_uid_get(id, table, url):
    cursor = OauthToken.raw_sql('select name,uid from %s where id=%%s'%table, id)
    r = cursor.fetchone()
    if r:
        name, uid = r
        return (name, url%uid)
    return (None, None)

def oauth_name_link(app_id, id):
    if app_id in OAUTH2URL:
        table = OAUTH2TABLE[app_id]
        url = OAUTH2URL[app_id]
        r = name_uid_get(id, table, url)
    else:
        r = (None, None)
    return r


#from binascii import crc32
#from hashlib import md5
#
#
#def renren_mail_hash(s):
#    s = s.strip().lower()
#    c = crc32(s) & 0xffffffff
#    m = md5(s).hexdigest()
#    return '%08d_%s' % (c, m)
#
#
#def renren_mail_by_hash(s):
#    db = cursor_by_table("renren_mail_hash")
#    c = db.cursor()
#    c.execute('select mail from renren_mail_hash where hash=%s', s)
#    r = c.fetchone()
#    if r:
#        return c[0]


if __name__ == '__main__':
    oauth_by_zsite_id(10017321)
    #oauth_save(OAUTH_BUZZ, 2, '2', '1')
    #print oauth_sync_sum('11')

#def oauth_url(
#url, api_key, api_secret, access_token, access_token_secret, parameters={}, method="GET", data=None
#)
#
#->
#
#gae 来 urlfetch
#
#好处
#twttier
#不用翻墙
