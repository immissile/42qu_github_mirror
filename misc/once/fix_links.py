#coding:utf-8
import _env
from model.oauth import OAUTH_DOUBAN, OAUTH_SINA, OAUTH_TWITTER, OAUTH_QQ
from model.zsite_link import ZsiteLink

OAUTH2NAME_DICT = {
    OAUTH_QQ        : '腾讯微博'    ,
    OAUTH_DOUBAN    : '豆瓣'        ,
    OAUTH_SINA      : '新浪微博'    ,
    OAUTH_TWITTER   : 'Twitter'     ,
}

OAUTH2URL = {
    OAUTH_DOUBAN:'http://www.douban.com/people/%s/',
    OAUTH_SINA:'http://weibo.com/%s',
    OAUTH_TWITTER:'http://twitter.com/%s',
    OAUTH_QQ:'http://t.qq.com/%s',
}


def validate_all_links():
    c = ZsiteLink.raw_sql('select id, cid, link from zsite_link where cid=2 or cid=3 or cid=4 or cid=8')
    x = c.fetchall()
    for i in x:
        id = i[0]
        cid = i[1]
        link = i[2]
        validate_link(id, cid, link)

def validate_link(id, cid, link):
    pure_link = link[7:].strip('@')
    try:
        if ord(pure_link[0]) > 127 or '@' in pure_link:
            print pure_link
            print ''
    except:
        pass

    if pure_link.isalnum():
        print 'id:%s cid:%s EX:%s' % (id, cid, pure_link)
        pure_link = OAUTH2URL[cid] % pure_link
        print pure_link
        print ''
        ZsiteLink.raw_sql('update zsite_link set link=%s where id=%s' , pure_link, id)

if __name__ == '__main__':
    validate_all_links()
