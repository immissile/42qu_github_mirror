#!/usr/bin/env python
# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup, Tag, NavigableString

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
                if name == 'img':
                    src = i.get('src')
                    if src:
                        print src
                        if src not in pic_list:
                            pic_seq = len(pic_list) + 1
                            pic_list.append(src)
                        else:
                            pic_seq = pic_list.index(src) + 1
                        li.append(u'\n图:%s\n' % pic_seq)
                else:
                    s = soup2txt_recursion(i)

                    if name in BLOCK_BOLD:
                        li.append(u'\n**%s**\n' % s)
                    elif name in BLOCK:
                        li.append(u'\n%s\n' % s)
                    elif name in BOLD:
                        li.append(u'**%s**' % s)
                    else:
                        li.append(s)
        return u''.join(li)

    s = soup2txt_recursion(soup)
    return '\n'.join(filter(bool, [i.strip() for i in s.splitlines()])), pic_list
