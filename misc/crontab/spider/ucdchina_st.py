#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from yajl import loads
from zkit.htm2txt import htm2txt

def main():
    author_dict = {}
    with open("ucdchina_st.data") as f:
        for line in f:
            data = loads(line)
            author = htm2txt(data[2].replace("&nbsp;",''))[0]
            blog = data[3]
            title = data[0]

            if author in author_dict:
                author_dict[author][0]+=1
                author_dict[author][2]+=" %s"%title
            else:
                author_t=[None]*3
                author_dict[author]=author_t
                author_t[0]=1
                author_t[1]=blog
                author_t[2]=title

    author_dict = sorted(author_dict.iteritems(),key=lambda x:x[1][0],reverse=True)
    for k,v in author_dict:
        print v[0],k,v[1],v[2]

if __name__ == '__main__':
    main()
