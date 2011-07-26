from model.oauth import OAUTH_GOOGLE, OAUTH_DOUBAN, OAUTH_SINA, OAUTH_TWITTER, OAUTH_WWW163, OAUTH_BUZZ, OAUTH_SOHU, OAUTH_QQ, OAUTH_RENREN, OAUTH_LINKEDIN
from model.oauth import OAUTH2NAME_DICT, OAUTH2URL
from model.zsite_link import ZsiteLink

OAUTH2NAME_DICT = {
    OAUTH_GOOGLE    : 'Google'      ,
    OAUTH_WWW163    : '网易微博'    ,
    OAUTH_SOHU      : '搜狐微博'    ,
    OAUTH_QQ        : '腾讯微博'    ,
    OAUTH_RENREN    : '人人网'      ,
    OAUTH_DOUBAN    : '豆瓣'        ,
    OAUTH_SINA      : '新浪微博'    ,
#    OAUTH_BUZZ      : 'Buzz'        ,
    OAUTH_TWITTER   : 'Twitter'     ,
    OAUTH_LINKEDIN  : 'LinkedIn'    ,
}

OAUTH2URL = {
    OAUTH_DOUBAN:'http://www.douban.com/people/%s/',
    OAUTH_SINA:'http://t.sina.com.cn/%s',
    OAUTH_TWITTER:'http://twitter.com/%s',
    OAUTH_WWW163:'http://t.163.com/%s',
    OAUTH_SOHU:'http://t.sohu.com/%s',
#    OAUTH_BUZZ:'%s',
    OAUTH_QQ:'http://t.qq.com/%s',
}


