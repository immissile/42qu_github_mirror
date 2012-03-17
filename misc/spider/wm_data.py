#coding:utf-8
from json import loads
from datetime import datetime
import _env
from model.days import time_by_string, int_by_string
from model._db import Model
from time import time

class SpiderWm(Model):
    pass

class SpiderWmUser(Model):
    pass

class SpiderWmFav(Model):
    pass

def wm_user_id(user):
    u = SpiderWmUser.get(name=user)
    if u is None:
        u = SpiderWmUser(name=user)
        u.save()
    return u.id

def wm_fav(user_id, wm_id):
    smu = SpiderWmFav.get_or_create(user_id=user_id, wm_id=wm_id)
    smu.save()

def wm_save(id, like, name, author, link, create_time, txt):
    wm = SpiderWm.get(wmid=id)
    if wm:
        return wm 

    now = time() 

    if '前' in create_time:
        create_time = now
    else:
        create_time = int_by_string(create_time)

    like = int(like or 0)

    wm = SpiderWm(
        wmid=id,
        like=like, name=name, author=author, link=link, time=create_time, txt=txt
    )
    wm.save()
    return wm
    
if __name__ == '__main__':
    pass


