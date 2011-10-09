# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup, Tag, NavigableString
import htmlentitydefs, re

BLOD_LINE = re.compile(r"^\s*\*\*[\r\n]+", re.M)

_char = re.compile(r'&(\w+?);')
_dec = re.compile(r'&#(\d{2,4});')
_hex = re.compile(r'&#x(\d{2,4});')

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
                    if s:
                        li.append(s)
                        href = i.get('href')
                        if href and href.startswith("http"):
                            li.append('[[%s]]'%href)
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
    print htm2txt("""
3
12345<a href="http://bw.com"><img src="$"></a>323
w
""")[0]

