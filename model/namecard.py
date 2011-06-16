#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache

STATE_DEL = 3
STATE_APPLY = 5
STATE_ACTIVE = 10

class Namecard(McModel):
    pass

mc_namecard_id = McCache('NamecardId.%s')

@mc_namecard_id('{user_id}')
def namecard_get_id(user_id):
    for i in Namecard.where(user_id=user_id, state=STATE_ACTIVE):
        return i.id
    return 0

def namecard_get(user_id):
    id = namecard_get_id(user_id)
    return Namecard.mc_get(id)

def namecard_new(
    user_id, sex, marry, birthday, pid_home, pid_now, name, phone, mail, address, state=STATE_ACTIVE
):
    c = namecard_get(user_id)
    if c:
        if \
            c.birthday == birthday and \
            c.pid_now == pid_now and \
            c.pid_home == pid_home and \
            c.name == name and \
            c.phone == phone and \
            c.mail == mail and \
            c.address == address and\
            c.marry == marry and\
            c.sex == sex:
            return c
        c.state = STATE_DEL
        c.save()

    c = Namecard(
        birthday=birthday or None,
        user_id=user_id,
        pid_now=pid_now,
        pid_home=pid_home,
        name=name,
        phone=phone,
        mail=mail,
        address=address,
        state=state,
        sex=sex,
        marry=marry
    )
    c.save()
    mc_namecard_id.set(user_id, c.id)
    return c

if __name__ == '__main__':
    pass

