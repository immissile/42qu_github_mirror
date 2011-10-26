#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from zkit.single_process import single_process
from model.kv_misc import kv_int, KV_INVITE_MESSAGE
from model.invite_email import InviteMessage, InviteEmail
from model.mail import rendermail
from model.zsite import Zsite
from model.invite_email import INVITE_CID2CN

@single_process
def invite_message():
    pre_pos = 0 #kv_int.get(KV_INVITE_MESSAGE)
    c = InviteMessage.raw_sql(
            'select max(id) from invite_message'
            )
    pos = c.fetchone()[0]

    if pos > pre_pos:
        for m in InviteMessage.where('id>%s and id<=%s',pre_pos,pos):
            print m.email
            #rendermail(
            #        '/mail/invite/invite_message.txt',
            #        m.email,name,
            #        invitor = Zsite.mc_get(m.uid),
            #        cid = INVITE_CID2CN[abs(cids)]
            #        )


        kv_int.set(KV_INVITE_MESSAGE, pos)


if __name__ == "__main__":
    invite_message()
