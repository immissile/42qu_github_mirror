#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache
from zkit.city import pid_hex2int

STATE_DEL = 3
STATE_APPLY = 5
STATE_ACTIVE = 10

class Namecard(McModel):
    pass

mc_namecard_id = McCache('NamecardId.%s')

@mc_namecard_id('{user_id}')
def get_namecard_id(user_id):
    for i in Namecard.where(user_id=user_id, state=STATE_ACTIVE):
        return i.id
    return 0

def get_namecard(user_id):
    id = get_namecard_id(user_id)
    return Namecard.mc_get(id)

def namecard_new(user_id, pid, phone, mail, address, state=STATE_ACTIVE):
    pid = pid_hex2int(pid)
    c = get_namecard(user_id)
    if c:
        if c.pid == pid and c.phone == phone and c.mail == mail and c.address == address:
            return c
        c.state = STATE_DEL
        c.save()
    c = Namecard(
        user_id=user_id,
        pid=pid,
        phone=phone,
        mail=mail,
        address=address,
        state=state,
    )
    c.save()
    mc_namecard_id.set(user_id, c.id)
    return c

if __name__ == '__main__':
    pass
