#!/usr/bin/env python
# coding: utf-8 

from _db import redis
from model.zsite import Zsite , CID_USER
from model.autocomplete import AutoComplete, redis
from model.zsite_url import url_by_id
from model.user_mail import mail_by_user_id
from model.follow import follow_count_by_to_id

def tag_alias_by_id_query(id, query):
    url = url_by_id(id)
    if query in url.lower():
        return url

    mail = mail_by_user_id(id)

    if query == mail:
        return mail
    elif query in mail:
        return mail.rsplit("@",1)[0]

    return 0

autocomplete_user = AutoComplete('user', tag_alias_by_id_query)

def autocomplete_user_name_new(user, rank=None):
    name = user.name
    id = user.id
    if rank is None:
        rank = follow_count_by_to_id(id)
    autocomplete_user.append(name, id, rank)

def autocomplete_user_mail_new(user, mail, rank=None):
    id = user.id
    if rank is None:
        rank = follow_count_by_to_id(id)
    autocomplete_user.append_alias( mail.split('@', 1)[0], id, rank )
    autocomplete_user.add(mail, id, rank)

def autocomplete_user_url_new(user, url, rank=None):
    id = user.id
    if rank is None:
        rank = follow_count_by_to_id(id)
    autocomplete_user.append_alias( url, id, rank )

    
def autocomplete_user_new(user):
    from model.user_mail import mail_by_user_id
    id = user.id
    rank = follow_count_by_to_id(id)

    autocomplete_user_name_new(user, rank)
    autocomplete_user_mail_new(user, mail_by_user_id(id), rank )
    url = url_by_id(id)
    if url:
        autocomplete_user_url_new(user, url, rank)

if __name__ == '__main__':
    pass
    print autocomplete_user.id_rank_name_list_by_str('z')
