#coding:utf-8
from json import loads
from datetime import datetime
import _env
from model.days import time_by_string
from model._db import Model


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

def wm_save(id, like, name, author, link, time, txt):
    wm = SpiderWm.get(wmid=id)
    if wm:
        return wm 

    now = datetime.today()

    id, like, name, author, link, time, txt = loads(line)
    if '前' in time:
        time = now
    else:
        time = time_by_string(time)

    like = int(like or 0)

    wm = SpiderWm(
        wmid=id,
        like=like, name=name, author=author, link=link, time=time, txt=txt
    )
    wm.save()
    return wm
    
if __name__ == '__main__':
    pass



