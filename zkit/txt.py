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
    txt = str(txt)
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
1、请你自我介绍一下你自己？
回答提示：一般人回答这个问题过于平常，只说姓名、年龄、爱好、工作经验，这些在简历上都有。其实，企业最希望知道的是求职者能否胜任工作，包括：最强的技能、最深入研究的知识领域、个性中最积极的部分、做过的最成功的事，主要的成就等，这些都可以和学习无关，也可以和学习有关，但要突出积极的个性和做事的能力，说得合情合理企业才会相信。企业很重视一个人的礼貌，求职者要尊重考官，在回答每个问题之后都说一句“谢谢”，企业喜欢有礼貌的求职者。

2、你觉得你个性上最大的优点是什么？
回答提示：沉着冷静、条理清楚、立场坚定、顽强向上、乐于助人和关心他人、适应能力和幽默感、乐观和友爱。我经过一到两年的培训及项目实战，加上实习工作，使我适合这份工作。

""")
