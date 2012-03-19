#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel
from zkit.earth import place_name
from zkit.astrology import astrology
from zkit.attrcache import attrcache
from days import today_year

MARRY_ONE = 1

class UserInfo(McModel):
    @attrcache
    def place_home(self):
        return place_name(self.pid_home)

    @property
    def age(self):
        birthday = self.birthday
        if birthday:
            year = birthday//10000
            if year:
                return today_year() - year

    @property
    def astrology(self):
        return astrology(self.birthday)

def user_info_new(
    user_id,
    birthday=0,
    marry=0,
    pid_home=0,
    sex=0,
):
    o = UserInfo.get_or_create(id=user_id)
    if birthday:
        o.birthday = birthday
    if sex:
        o.sex = sex
    o.marry = marry
    if pid_home:
        o.pid_home = pid_home
    o.save()
    return o

#1为男 , 2为女
def user_sex(user_id):
    o = UserInfo.mc_get(user_id)
    if o:
        sex = o.sex
    else:
        sex = 0
    return sex

if __name__ == '__main__':
    pass
    n = UserInfo.mc_get(10001299)
    print n
    print type(n.pid_home)
#    n.sex=2
#    n.marry=0
#    n.save()



