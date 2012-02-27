#!/usr/bin/env python
# -`- coding: utf-8 -`-

from _db import redis
from model.zsite import Zsite , CID_USER
from model.autocomplete import AutoComplete
from model.zsite_url import url_by_id
from model.user_mail import mail_by_user_id
from model.follow import follow_count_by_to_id
 
def tag_alias_by_id_query(id, query):
    url = url_by_id(id)  
    if query in url:
        return url
     
    return 0 

autocomplete_user = AutoComplete("user", tag_alias_by_id_query)

def autocomplete_user_name_new(user, rank=None):
    name = user.name
    id = user.id
    if rank is None:
        rank = follow_count_by_to_id(id)
    autocomplete_user.append(name, id, rank)

    

if __name__ == '__main__':
    pass
    print autocomplete_user.id_rank_name_list_by_str('t')
#    for i in Zsite.where(cid=CID_USER):
#        print i.name

