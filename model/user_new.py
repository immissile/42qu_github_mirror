# -*- coding: utf-8 -*-

from user_info import user_info_new
from user_auth import  user_new_by_mail
from search_zsite import search_new

def user_new(mail, password=None, name=None, sex=0):
    user = user_new_by_mail(mail, password, name)
    user_id = user.id
    user_info_new(user_id, sex=sex)
    search_new(user_id)
    return user_id


if __name__ == '__main__':
    #from zsite import Zsite
    #z = Zsite.mc_get(10001229)
    #print z.name
    user_id = user_new('g.u.oha.o.chua.n@gmail.com', sex=1)
