#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup, Tag, NavigableString
from fetch_pic import fetch_pic


BOLD = ['b', 'strong', 'i', 'em']
BOLD.extend(['h%s' % i for i in range(1,7)])
PASS = ['span']

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
                if name == 'p':
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

from model.po import po_note_new
from model.po_pic import po_pic_new
from model.state import STATE_SECRET

def htm2po(user_id, title, htm):
    po = po_note_new(user_id, title, '', STATE_SECRET)
    po_id = po.id
    try:
        txt, pic_list = htm2txt(htm)
    except:
        po.txt_set(htm)
    else:
        for seq, url in enumerate(pic_list, 1):
            img = fetch_pic(url)
            if img:
                po_pic_new(user_id, po_id, img, seq)
        po.txt_set(txt)
    return po
