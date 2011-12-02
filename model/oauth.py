#coding:utf-8
from _db import cursor_by_table, McNum, Model, McCache
from model.zsite_url import  RE_URL

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
OAUTH_KAIXIN = 11
OAUTH_FANFOU = 12
OAUTH_MY = 100

OAUTH2NAME_DICT = {
    OAUTH_MY        : '官方网站'    ,
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
    OAUTH_KAIXIN    : '开心'        ,
    OAUTH_FANFOU    : '饭否'        ,
}
OAUTH2NAME_DICT_SHORT = {
    OAUTH_WWW163    : '网易'    ,
    OAUTH_SOHU      : '搜狐'    ,
    OAUTH_QQ        : '腾讯'    ,
    OAUTH_RENREN    : '人人'      ,
    OAUTH_DOUBAN    : '豆瓣'        ,
    OAUTH_SINA      : '新浪'    ,
    OAUTH_KAIXIN    : '开心'  ,
    OAUTH_FANFOU    : '饭否' ,
}

OAUTH_TUPLE = (
    OAUTH_DOUBAN    ,
    OAUTH_SINA      ,
    OAUTH_QQ        ,
    OAUTH_RENREN    ,
    OAUTH_KAIXIN  ,
    OAUTH_WWW163    ,
    #OAUTH_SOHU      ,
    #OAUTH_TWITTER   ,
    OAUTH_FANFOU,
)



OAUTH2URL = {
    OAUTH_DOUBAN:'http://www.douban.com/people/%s/',
    OAUTH_SINA:'http://t.sina.com.cn/%s',
    OAUTH_TWITTER:'http://twitter.com/%s',
    OAUTH_WWW163:'http://t.163.com/%s',
    OAUTH_SOHU:'http://t.sohu.com/%s',
    OAUTH_RENREN:'http://www.renren.com/profile.do?id=%s',
#    OAUTH_BUZZ:'%s',
    OAUTH_QQ:'http://t.qq.com/%s',
    OAUTH_KAIXIN:'http://www.kaixin001.com/home/?uid=%s',
    OAUTH_FANFOU:'http://fanfou.com/%s'
}

OAUTH2TABLE = {
    #OAUTH_BUZZ:"oauth_token_buzz",
    OAUTH_TWITTER:'oauth_token_twitter',
    OAUTH_SOHU:'oauth_token_sohu',
    OAUTH_SINA:'oauth_token_sina',
    OAUTH_DOUBAN:'oauth_token_douban',
    OAUTH_WWW163:'oauth_token_www163',
    OAUTH_QQ:'oauth_token_qq',
    OAUTH_RENREN:'oauth_token_renren',
    OAUTH_KAIXIN:'oauth_token_kaixin',
    OAUTH_FANFOU:'oauth_token_fanfou'
}


OAUTH_SYNC_CID = set(
    OAUTH2NAME_DICT.iterkeys()
)

OAUTH_SYNC_SQL = 'app_id in (%s)' % (','.join(map(str, OAUTH_SYNC_CID)))

OAUTH_SYNC_TXT = '42区 , 找到给你答案的人 -> http://42qu.com'

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

mc_oauth_name_by_oauth_id = McCache('OauthNameByOauthId:%s')

@mc_oauth_name_by_oauth_id('{oauth_id}')
def oauth_name_by_oauth_id(app_id, oauth_id):
    table = OAUTH2TABLE[app_id]
    cursor = cursor_by_table(table)
    cursor.execute('select name from %s where id=%%s'%table, oauth_id)
    r = cursor.fetchone()
    if r:
        return r[0]



def oauth_rm_by_oauth_id(oauth_id):
    cursor = cursor_by_table('oauth_token')
    cursor_new = cursor_by_table('oauth_token_backup')
    cursor.execute('select id,app_id,zsite_id,token_key,token_secret from oauth_token where id=%s', oauth_id)
    item = cursor.fetchone()
    if item:
        cursor_new.execute('insert into oauth_token_backup (id,app_id,zsite_id,token_key,token_secret) values (%s,%s,%s,%s,%s)', item)
        cursor.execute('delete from oauth_token where id =%s', oauth_id)



def oauth_save(app_id, zsite_id, token_key, token_secret):


    cursor = OauthToken.raw_sql(
        'select id from oauth_token where zsite_id=%s and app_id=%s and token_key=%s and token_secret=%s',
        zsite_id, app_id, token_key, token_secret
    )
    r = cursor.fetchone()
    if r:
        #oauth_rm_by_oauth_id(r[0])
        return r[0]

    id = OauthToken.raw_sql(
        'insert into oauth_token (app_id,zsite_id,token_key,token_secret) values (%s,%s,%s,%s)',
        app_id, zsite_id, token_key, token_secret
    ).lastrowid

    if app_id in OAUTH_SYNC_CID:
        oauth_sync_sum.delete(zsite_id)

    return id



def oauth_save_google(zsite_id, token_key, token_secret):
    return oauth_save(OAUTH_GOOGLE, zsite_id, token_key, token_secret)

def oauth_save_renren(zsite_id, token_key, refresh_token, name, uid):
    return oauth_save_with_uid(OAUTH_RENREN, zsite_id, token_key, refresh_token, name, uid)

def oauth_save_with_uid(app_id, zsite_id, token_key, token_secret, name, uid):
    id = oauth_save(app_id, zsite_id, token_key, token_secret)
    name_uid_set(id, name, uid, OAUTH2TABLE[app_id])
    from model.zsite_link import  link_cid_new
    link_cid_new(zsite_id, app_id, (OAUTH2URL[app_id])%uid)
    return id

#def oauth_save_buzz(zsite_id, token_key, token_secret, name, uid):
#    oauth_save_with_uid(OAUTH_BUZZ, zsite_id, token_key, token_secret, name, uid)

def oauth_save_twitter(zsite_id, token_key, token_secret, name, uid):
    return oauth_save_with_uid(OAUTH_TWITTER, zsite_id, token_key, token_secret, name, uid)

def oauth_save_sohu(zsite_id, token_key, token_secret, name, uid):
    return oauth_save_with_uid(OAUTH_SOHU, zsite_id, token_key, token_secret, name, uid)

def oauth_save_qq(zsite_id, token_key, token_secret, name, uid):
    return oauth_save_with_uid(OAUTH_QQ, zsite_id, token_key, token_secret, name, uid)

def oauth_save_sina(zsite_id, token_key, token_secret, name, uid):
    return oauth_save_with_uid(OAUTH_SINA, zsite_id, token_key, token_secret, name, uid)

def oauth_save_douban(zsite_id, token_key, token_secret, name, uid):
    return oauth_save_with_uid(OAUTH_DOUBAN, zsite_id, token_key, token_secret, name, uid)

def oauth_save_www163(zsite_id, token_key, token_secret, name, uid):
    return oauth_save_with_uid(OAUTH_WWW163, zsite_id, token_key, token_secret, name, uid)

def oauth_save_kaixin(zsite_id, token_key, token_secret, name, uid):
    return oauth_save_with_uid(OAUTH_KAIXIN, zsite_id, token_key, token_secret, name, uid)

def oauth_save_fanfou(zsite_id, token_key, token_secret, name, uid):
    return oauth_save_with_uid(OAUTH_FANFOU, zsite_id, token_key, token_secret, name, uid)

def oauth_by_zsite_id(zsite_id):
    cursor = OauthToken.raw_sql(
        'select app_id,id from oauth_token where zsite_id=%s order by id desc', zsite_id
    )
    return cursor.fetchall()

def oauth_by_zsite_id_last(zsite_id):
    r = oauth_by_zsite_id(zsite_id)
    if r:
        return r[0]

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

def linkify(link, cid=0):
    link = link.strip().split(' ', 1)[0]
    if link:
        if cid in OAUTH2URL and RE_URL.match(link):
            link = OAUTH2URL[cid] % link
        elif not link.startswith('http://') and not link.startswith('https://'):
            link = 'http://%s'%link
    return link

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

def token_key_login_set(app_id, token_key, zsite_id):
    cursor = OauthToken.raw_sql(
        'select id from oauth_token where app_id=%s and token_key=%s and (zsite_id=0 or zsite_id=%s)',
         app_id, token_key , zsite_id
    )
    r = cursor.fetchone()
    if r and r[0]:
        id = r[0]
        OauthToken.raw_sql('update oauth_token set (zsite_id, login) values (%s, 1) where id=%s', zsite_id, id) 
     
def mail_by_token_key_login(app_id, token_key):
    cursor = OauthToken.raw_sql(
        'select zsite_id from oauth_token where app_id=%s and token_key=%s limit 1',
         app_id, token_key 
    )
    r = cursor.fetchone()
    if r:
        from model.user_mail import mail_by_user_id
        return mail_by_user_id(r[0])

def zsite_id_by_token_key_login(app_id, token_key):
    cursor = OauthToken.raw_sql(
        'select zsite_id from oauth_token where app_id=%s and token_key=%s and login=1',
         app_id, token_key 
    )
    r = cursor.fetchone()
    if r:
        return r[0]

def oauth_token_key_by_id(id):
    cursor = OauthToken.raw_sql(
        'select token_key from oauth_token where id=%s', id
    )
    r = cursor.fetchone()
    if r:
        return r[0]



if __name__ == '__main__':
#    print http://zuroc.xxx/auth/bind/73?key=140505-98e90d530cb976ebd7242a9282f32c17
    print oauth_token_key_by_id(73)
    #oauth_save(OAUTH_BUZZ, 2, '2', '1')
    #print oauth_sync_sum('11')
    pass
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
