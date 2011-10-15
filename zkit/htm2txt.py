# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup, Tag, NavigableString
import htmlentitydefs, re
BLOD_LINE = re.compile(r"^\s*\*\*[\r\n]+", re.M)

_char = re.compile(r'&(\w+?);')
_dec = re.compile(r'&#(\d{2,4});')
_hex = re.compile(r'&#x(\d{2,4});')
RE_TU = re.compile(r"^\s*图:\d+\s*$")

def _char_unescape(m, defs=htmlentitydefs.entitydefs):
    try:
        return defs[m.group(1)]
    except KeyError:
        return m.group(0)


import re, htmlentitydefs
def unescape(s):
    # First convert alpha entities (such as &eacute;)
    # (Inspired from http://mail.python.org/pipermail/python-list/2007-June/443813.html)
    def entity2char(m):
        entity = m.group(1)
        if entity in htmlentitydefs.name2codepoint:
            return unichr(htmlentitydefs.name2codepoint[entity])
        return u" "  # Unknown entity: We replace with a space.
    t = re.sub(u'&(%s);' % u'|'.join(htmlentitydefs.name2codepoint), entity2char, s)

    # Then convert numerical entities (such as &#233;)
    t = re.sub(u'&#(\d+);', lambda x: unichr(int(x.group(1))), t)

    # Then convert hexa entities (such as &#x00E9;)
    return re.sub(u'&#x(\w+);', lambda x: unichr(int(x.group(1), 16)), t)


BLOCK_BOLD = set([
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
])

BLOCK = set([
    'form',
    'hr',
    'div',
    'table',
    'tr',
    'li',
    'pre',
    'p',
])

BOLD = set([
    'b',
    'strong',
    'i',
    'em',
])

PASS = set([
    'span',
    'font',
])

def htm2txt(htm):
    htm = htm.replace(u'*', u'﹡')

    soup = BeautifulSoup(htm)

    pic_list = []

    def soup2txt_recursion(soup):
        li = []
        for i in soup:

            if isinstance(i, NavigableString):

                li.append(i.string)

            else:

                name = i.name
                if name == 'a':
                    s = soup2txt_recursion(i)
                    ss = s.rstrip()
                    if not RE_TU.match(ss.lstrip().encode('utf-8')):
                        li.append(ss)
                        href = i.get('href')
                        if href and href.startswith('http'):
                            li.append('[[%s]]'%href)
                        li.append(s[len(ss):])
                    else:
                        li.append(s)
                elif name == 'img':
                    src = i.get('src')
                    if src:
                        #print src
                        if src not in pic_list:
                            pic_seq = len(pic_list) + 1
                            pic_list.append(src)
                        else:
                            pic_seq = pic_list.index(src) + 1
                        li.append(u'\n图:%s\n' % pic_seq)
                else:
                    s = soup2txt_recursion(i)

                    if name in BLOCK_BOLD:
                        if '\n' not in s:
                            li.append(u'\n**%s**\n' % s)
                        else:
                            li.append(s)
                    elif name in BLOCK:
                        li.append(u'\n%s\n' % s)
                    elif name in BOLD:
                        li.append(u'**%s**' % s)
                    else:
                        li.append(s)

        return u''.join(li)

    s = soup2txt_recursion(soup)
    s = unescape(s.strip())
    txt = '\n\n'.join(filter(bool, [i.strip() for i in s.splitlines()]))
    txt = BLOD_LINE.sub('**', txt)
    return txt , pic_list

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    print htm2txt("""
<p>1.结合蓝牙4.0或者耳机唤醒手机。语音搜索和语音输入等技术都要用户手动点击按钮触发语音功能，这事本身就不够酷。但是不借助设备还存在困难，语音功能实时开启探测声波会耗费电量。</p>
<a href="http://s.click.taobao.com/t_8?e=7HZ6jHSTbIKlPmx3I8jQNkStCTbEkQKlZsvg9GbV%2FWqDj5qh0SFCLeoyLzeq8YtJ18fjoRevav0Je6BzSvsi2e8Oqn1r%2BKdXSyoYFAxWa054G4DkCA%3D%3D&amp;p=mm_12328700_0_0&amp;n=19&amp;u=17f3980" rel="nofollow"><img src="http://www.chong4.com.cn/image/readmore.gif">点击这里购买&mdash;&mdash;流苏不规则毛衣披肩</a>
""")[0]

