#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from model._db import cursor_by_table

cursor = cursor_by_table('vps')

PORT_SSH_OFFSET = 50000


STATE_VPS_TO_OPEN = 10  #等待开通
STATE_VPS_OPENED = 20   #已经开通
STATE_VPS_TO_CLOSE = 30 #等待关闭
STATE_VPS_CLOSED = 40   #已经关闭


def vps

def main():
    cursor.execute("select id, id_in_group, `group` from vps where state=%s", STATE_VPS_TO_OPEN)
    for id, state, ssh_port, group in cursor.fetchall():
        #TODO
        cursor.execute("update state=%s where id=%s", (STATE_VPS_OPENED, id))


    cursor.execute("select id, id_in_group, `group` from vps where state=%s", STATE_VPS_TO_CLOSE)
    for id, state, ssh_port, group in cursor.fetchall():
        ssh_port = id_in_group+ PORT_SSH_OFFSET
        #TODO
        cursor.execute("update state=%s where id=%s", (STATE_VPS_CLOSED, id))


if "__main__" == __name__:
    main()

