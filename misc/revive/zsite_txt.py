#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from qu.mysite.model.man import Man
from model.zsite import Zsite

def main():
    for i in Zsite.where().col_list():
        man = Man.get(i)
# if man:
#     txt_new(i, man.txt)

if __name__ == '__main__':
    main()
