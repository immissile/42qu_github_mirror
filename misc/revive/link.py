#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from qu.mysite.model.man_link import man_link_by_man_id 
from model.zsite_list_0 import zsite_show_new
from model.zsite import Zsite


def main():
    for zsite_id in Zsite.where().col_list():
        for name,link in man_link_by_man_id(zsite_id): 
            print name, link
        


if __name__ == '__main__':
    main()

