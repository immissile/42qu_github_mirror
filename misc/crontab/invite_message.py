#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from zkit.single_process import single_process
from model.kv_misc import kv_int, KV_INVITE_MESSAGE
from model.invite_email import InviteMessage
from model.mail import rendermail
from model.zsite import Zsite
from model.invite_email import INVITE_CID2CN
from json import loads

@single_process
def invite_message():
    pre_pos = kv_int.get(KV_INVITE_MESSAGE)
    #print pre_pos
    c = InviteMessage.raw_sql( 'select max(id) from invite_message')
    pos = c.fetchone()[0]
    if pos > pre_pos:
        for m in InviteMessage.where('id>%s and id<=%s', pre_pos, pos):
            email_list = loads( m.email )
            invitor = Zsite.mc_get(m.user_id)

            txt = m.txt

            for email in email_list:
                if '@' not in email:
                    continue
                email = email.split(' ', 1)
                if len(email) == 2:
                    email , name = email
                else:
                    email = email[0]
                    name = email.split('@', 1)[0]

                #print email
                #raw_input(email)
                #email = "zsp007@gmail.com"

                rendermail(
                    '/mail/invite/invite_message.txt',
                    email,
                    name,
                    invitor=invitor,
                    sender_name=invitor.name,
                    txt=txt
                )

        kv_int.set(KV_INVITE_MESSAGE, pos)


if __name__ == '__main__':
    invite_message()

