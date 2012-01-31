#!/usr/bin/env python
# -*- coding: utf-8 -*-

def sp_txt(txt):
    if str(txt).replace(' ', '').isalnum():
        yield txt
    else:
        txt = txt.decode('utf-8', 'ignore')
        for i in range(len(txt)-1):
            yield txt[i:i+2]

if __name__ == '__main__':
    for i in sp_txt('这是什么东西'):
        print i

    for i in sp_txt('a quick brown fox jumps over the lazy dog'):
        print i
