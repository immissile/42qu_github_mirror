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
            space = len(i) > 140

            if space and result and result[-1]:
                result.append('')

            result.append(i)

            if space:
                result.append('')

            pre = True
        elif result and result[-1]:
            result.append(i)
            has_split = True

    txt = '\n'.join(result)
    return txt

#<span style="margin-left:4px"><a href="#">显示全部</a></span>
if __name__ == '__main__':
    print mail_link('zsp007@gmail.com')
    print mail_link('zsp007@42qu.com')
    print format_txt("""

卡拉高一时因父亲工作调转而迁入一所新学校，学校里的同学都不愿意搭理她。卡拉为了能融入她们的圈子中，不惜一切。她改变自己的穿衣风格，重新购买新衣服，把“旧”衣服统统扔掉，力求和同学们保持一致；她请同学们喝汽水，吃冰激凌。当然这些统统由卡拉的父母出资，可依然收效甚微。于是，卡拉决定举办一次SPA聚会，邀请班里十五个女孩参加，费用预计要几千美元，卡拉的母亲开始要求卡拉把人数降到七人，而卡拉大哭大闹，不屈不挠地折腾了三个小时，母亲看到女儿伤心欲绝的模样，只好让步。聚会看上去似乎相当成功，女孩们都说自己很开心，卡拉露出了转学以来的第一个微笑。但她的微笑只持续到第二天上午。卡拉对她的同学们而言已经不具备利用价值，眨眼之间，昨天聚会上欢声笑语的女孩子重新开始对她冷若冰霜。 
　　她们无情地操纵了卡拉。这些女孩子知道，只要让卡拉保留一丝加入她们圈子的希望，她们就可以毫无顾忌地玩弄卡拉于股掌之上。当然，从另一方面说，卡拉也同样操纵了她的父母，特别是她的母亲。 
　　那么，为什么有人这么容易被操纵，操纵者会利用你的哪些弱点来控制你呢? 
　　你的性格存在哪些弱点： 
　　 
　　弱点之一：你想讨人欢心——拼命讨人欢心的习惯和心态 
　　如果你不幸有“讨人欢心”的心态，那么，你和他人的关系就不会那么简简单单了。你不是偶尔答应别人的请求，也不是偶尔为别人做好事，而是将自己的情绪始终和他人对你的期望保持高度一致，这终究会让你感到身心疲惫。 
　　 
　　弱点之二：没有别人的认可和赞许，你便活不下去 
　　如果你过度希望得到别人的肯定，对此感到不可或缺，那么，这时的你就很容易被他人操纵了。当你想得到别人肯定的时候，你就会像吸毒者那样，行为受控于人。操纵者只需做两步就可以了：第一步，给你想要的东西：第二步，威胁你要将这东西收回。 

 
　　第七步和解与协商 
　　可采用以下七个基本步骤： 
　　1、用简洁清晰的语言描述对方的立场：“我知道你希望／喜欢／期望……” 
　　2、确认你对其立场的理解是否正确，必要时请对方予以证实。 
　　3、用简洁清晰的语言表述自己的立场：“我希望／喜欢。” 
　　4、直接回答有关双方立场的问题，比如你希望时方采取何种行为、你对此的感受及这种行为的迫切性。 　　 
""")
