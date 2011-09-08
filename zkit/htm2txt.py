#!/usr/bin/env python
# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup, Tag, NavigableString

BLOCK_BOLD = [
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
]
BLOCK = [
    'form',
    'hr',
    'div',
    'table',
    'tr',
    'li',
    'pre',
    'p',
]
BOLD = [
    'b',
    'strong',
    'i',
    'em',
]
PASS = [
    'span',
]

def htm2txt(htm):
    soup = BeautifulSoup(htm)
    pic_list = []

    def soup2txt_recursion(soup):
        li = []
        for i in soup:
            if isinstance(i, NavigableString):
                li.append(i.string)
            else:
                name = i.name
                s = soup2txt_recursion(i)
                if name in BLOCK_BOLD:
                    li.append('\n**%s**\n' % s)
                elif name in BLOCK:
                    li.append('\n%s\n' % s)
                elif name in BOLD:
                    li.append('**%s**' % s)
                elif name in PASS:
                    li.append(s)
                elif name == 'img':
                    src = i.get('src')
                    if src:
                        if src not in pic_list:
                            pic_seq = len(pic_list) + 1
                            pic_list.append(src)
                        else:
                            pic_seq = pic_list.index(src) + 1
                        li.append(' 图:%s ' % pic_seq)
        return ''.join(li)

    s = soup2txt_recursion(soup)
    return '\n'.join(filter(bool, [i.strip() for i in s.splitlines()])), pic_list
