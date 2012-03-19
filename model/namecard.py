#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache
from state import STATE_RM, STATE_ACTIVE
from zkit.earth import place_name
from zkit.attrcache import attrcache
from zkit.mc_func import mc_func_get_dict


class Namecard(McModel):
    @attrcache
    def place_now(self):
        return place_name(self.pid_now)


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
    user_id,
    pid_now=0,
    name='',
    phone='',
    mail='',
    address='',
    state=STATE_ACTIVE
):
    c = namecard_get(user_id)
    if c:
        if \
            c.pid_now == pid_now and \
            c.name == name and \
            c.phone == phone and \
            c.mail == mail and \
            c.address == address:
            return c
        c.state = STATE_RM
        c.save()

    c = Namecard(
        user_id=user_id,
        pid_now=pid_now,
        name=name,
        phone=phone,
        mail=mail,
        address=address,
        state=state,
    )
    c.save()
    mc_namecard_id.set(user_id, c.id)
    return c

def namecard_dict(id_list):
    return mc_func_get_dict(
        mc_namecard_id,
        namecard_get_id,
        id_list,
    )

def namecard_bind(li, key='id'):
    d = set()
    for i in li:
        k = getattr(i, key)
        d.add(k)

    r = namecard_dict(d)
    id_list = r.values()
    e = Namecard.mc_get_dict(id_list)

    for i in li:
        i.namecard = e.get(r.get(getattr(i, key)))

if __name__ == '__main__':
    from zsite import Zsite
    li = Zsite.mc_get_list([10000212, 10000000])
    namecard_bind(li, 'id')
    for i in li:
        print vars(i)
        o = i.namecard
        print o.id, vars(o)
