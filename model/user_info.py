#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache


class UserInfo(McModel):
    pass


def user_info_new(
    user_id,
    birthday=0,
    marry=0,
    pid_home=0,
    sex=0,
):
    o = UserInfo.get_or_create(id=user_id)
    if birthday:
        o.birthday = birthday or '00000000'
    if sex:
        o.sex = sex
    o.marry = marry
    if pid_home:
        o.pid_home = pid_home
    o.save()
    return o
