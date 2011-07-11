#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from qu.mysite.model.man_link import man_link_by_man_id 
from model.zsite_list_0 import zsite_show_new
from model.zsite import Zsite
from model.oauth import OAUTH2NAME_DICT
from model.zsite_link import link_cid_new, ZsiteLink

dict_reverse = dict((i[1],i[0]) for i in OAUTH2NAME_DICT.items())

def main():
    for zsite_id in Zsite.where().col_list():
        for name,link in man_link_by_man_id(zsite_id):
            if name in dict_reverse:
                link_cid_new(zsite_id,dict_reverse[name],link)
            elif link:
                zsite_link = ZsiteLink.get_or_create(zsite_id=zsite_id, cid=0)
                zsite_link.link = link
                zsite_link.name = name
                zsite_link.save()
            print name, link
    


if __name__ == '__main__':
    main()

