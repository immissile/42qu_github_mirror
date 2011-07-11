#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from qu.mysite.model.man_show import ManShow
from model.zsite_list_0 import zsite_show_new

def main():
    for i in ManShow.where():
        print i.man_id, i.rank
        zsite_show_new(i.man_id, i.rank)

if __name__ == '__main__':
    main()

