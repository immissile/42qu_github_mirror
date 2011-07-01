#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache
from zkit.earth import place_name
from zkit.attrcache import attrcache


class UserInfo(McModel):
    @attrcache
    def place_home(self):
        return place_name(self.pid_home)


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
