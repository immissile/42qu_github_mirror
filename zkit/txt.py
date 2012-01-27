#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
EMAIL_VALID = re.compile(r'^\w+[-+.\w]*@\w+([-.]\w+)*\.\w+([-.]\w+)*$')

EMAIL_DICT = {
    'msn.com': ('MSN', 'http://login.live.com/'),
    '2008.sina.com': ('新浪', 'http://mail.2008.sina.com.cn/index.html'),
    'sina.com.cn': ('新浪', 'http://mail.sina.com.cn/index.html'),
    'vip.163.com': ('163', 'http://vip.163.com/'),
    'hongkong.com': ('中华邮', 'http://mail.china.com'),
    'sohu.com': ('搜狐', 'http://mail.sohu.com'),
    'live.com': ('Live', 'http://login.live.com/'),
    'eyou.com': ('亿邮', 'http://mail.eyou.com/'),
    'citiz.net': ('Citiz', 'http://citiz.online.sh.cn/citiz_index.htm'),
    'yeah.net': ('Yeah', 'http://mail.yeah.net/'),
    'vip.tom.com': ('Tom', 'http://vip.tom.com/'),
    'vip.qq.com': ('QQ', 'http://mail.qq.com/cgi-bin/loginpage?t=loginpage_vip&f=html'),
    'yahoo.com.hk': ('雅虎', 'http://mail.yahoo.com.hk'),
    'yahoo.cn': ('雅虎', 'http://mail.cn.yahoo.com/'),
    '188.com': ('188', 'http://www.188.com/'),
    '2008.china.com': ('中华邮', 'http://mail.china.com'),
    'vip.sohu.com': ('搜狐', 'http://mail.sohu.com'),
    '163.com': ('163', 'http://mail.163.com'),
    '126.com': ('126', 'http://www.126.com/'),
    'chinaren.com': ('chinaren', 'http://mail.chinaren.com'),
    'tom.com': ('Tom', 'http://mail.tom.com/'),
    'china.com': ('中华邮', 'http://mail.china.com'),
    '139.com': ('139', 'http://mail.139.com/'),
    'hotmail.com': ('Hotmail', 'http://www.hotmail.com'),
    '21cn.com': ('21cn', 'http://mail.21cn.com/'),
    'gmail.com': ('Gmail', 'http://mail.google.com'),
    'my3ia.sina.com': ('新浪', 'http://vip.sina.com.cn/index.html'),
    'yahoo.com.tw': ('雅虎', 'http://mail.yahoo.com.tw'),
    'vip.sina.com': ('新浪', 'http://vip.sina.com.cn/index.html'),
    'mail.china.com': ('中华邮', 'http://mail.china.com'),
    '263.net': ('263', 'http://mail.263.net/'),
    'yahoo.com': ('雅虎', 'https://login.yahoo.com/'),
    'foxmail.com': ('Foxmail', 'http://www.foxmail.com/'),
    'qq.com': ('QQ', 'http://mail.qq.com'),
    'sina.cn': ('新浪', 'http://vip.sina.com.cn/index.html'),
    'yahoo.com.cn': ('雅虎', 'http://mail.cn.yahoo.com/'),
    'sogou.com': ('搜狗', 'http://mail.sogou.com/'),
    'sina.com': ('新浪', 'http://mail.sina.com.cn/index.html'),
    'live.cn': ('Live', 'http://login.live.com/'),
}

import cgi
def mail2link(mail):
    return '<a href="%s" target="_blank">%s</a>' % (mail_link(mail), mail)

def mail_link(mail):
    mail = cgi.escape(mail)
    if mail and mail.find('@') > 0:
        e_domain = mail.split(str('@'))[1]
        link = EMAIL_DICT.get(e_domain)
        if link:
            return link[1]
    return 'http://%s'%mail.rsplit('@', 1)[-1]

def cnenlen(s):
    if type(s) is str:
        s = s.decode('utf-8', 'ignore')
    return len(s.encode('gb18030', 'ignore')) // 2

def cnencut(s, length):
    ts = type(s)
    if ts is str:
        s = s.decode('utf-8', 'ignore')
    s = s.encode('gb18030', 'ignore')[:length*2].decode('gb18030', 'ignore')
    if ts is str:
        s = s.encode('utf-8', 'ignore')
    return  s

def cnenoverflow(s, length):
    txt = cnencut(s , length)
    if txt != s:
        txt = '%s ...' % txt.rstrip()
        has_more = True
    else:
        has_more = False
    return txt, has_more


def format_txt(txt):
    txt = txt.replace('　', ' ').replace('\r\n', '\n').replace('\r', '\n').rstrip().rstrip("\n")
    txt = map(str.strip, txt.split('\n'))
    result = []
    
    has_split = False
    for i in txt:
        if i:
            result.append(i)
            pre = True
        elif result and result[-1]:
            result.append(i)
            has_split = True

    if has_split:
        split = "\n"
    else:
        split = "\n\n"
    txt = split.join(result)
    return txt

#<span style="margin-left:4px"><a href="#">显示全部</a></span>
if __name__ == '__main__':
    print mail_link('zsp007@gmail.com')
    print mail_link('zsp007@42qu.com')
    print format_txt("""
女友说,她的前男友大年三十坐在他们以前约会的地儿,抽了几支烟，坐了一小时。她问我：感动吗？
我说：不感动。


不要告诉我这个男生向你求过婚，只是你未答应。
亦不要告诉我他只是自惭形秽，配不上你如珠如宝。
　　
男生不像女生只懂承受
哪怕他再愚钝
在真正的爱情面前都充满攻击性
　　


我见过某男，不被女方家庭接纳
为与他心爱的女子约会，半夜跳墙爬楼
不料被女子父母发现，便躲入水缸
寒冬腊月，几乎冻死
终于感动老人
　　
我亦见过某男，地位卑贱，被视为与女友不对等
为不使爱人受委屈，与女友约定两年之期
两年后果然衣锦还乡
香车别墅抱得美人归
　　
　　

真正爱你的男生一定是这样的，或者精神强大，或者物质强大
你被感动或者打动，然后心甘情愿于这个男生白头偕老
　　
而如果他既做不到前者，又做不到后者
那么，相信我，他只是不够爱你
　　
　　
他对自己没有信心，不知道能否给你幸福
他对你没信心，不知道你能否永伴他晨昏
他对爱情没信心，不知道明天是否这热烈就会化为灰烬，痴痴变成笑柄
　　
他想来想去
还是守着这平淡的日月比较安全
还是找一个不需要他耗心费力的另一半比较安全
还是没有承诺没有压力，走一步看一步比较安全......
　　
而这一切，还是因为
只是因为，他还不够爱你
　　
　　

所以，你的前男友为你从十七岁等到二十多
我不感动
　　
你久未联系的前前男友隔山隔水打听到你的电话，称他虽已有妻有女但随时愿意为你离婚
我同样，不感动
　　
　　
我们所在的世界没有王母
你不是牛郎，我亦不是织女
你若真对我情深如此
当初我未嫁，你未娶
你干什么去了？ 

""")
