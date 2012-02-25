#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from model._db import cursor_by_table
import sys
import os

cursor = cursor_by_table('vps')

PORT_SSH_OFFSET = 50000


STATE_VPS_TO_OPEN = 10  #等待开通
STATE_VPS_OPENED = 20   #已经开通
STATE_VPS_TO_CLOSE = 30 #等待关闭
STATE_VPS_CLOSED = 40   #已经关闭


def vps_open(group, id_in_group, vm_id, passwd):
    ssh_port = id_in_group + PORT_SSH_OFFSET

def vps_close(group, id_in_group):
    pass



def main():
    def _(from_state, to_state, recall):
        cursor.execute("select id, id_in_group, `passwd`, `group` from vps where state=%s", from_state)
        for id,  id_in_group, passwd, group in cursor.fetchall():
            recall(group, id_in_group)
            cursor.execute("update state=%s where id=%s", (to_state, id))

    if len (sys.argv) <= 1:
        print "need param"
        os._exit (1)
    action = sys.argv[1]
    if action == 'open':
        _(STATE_VPS_TO_OPEN, STATE_VPS_OPENED, vps_open)
    else:
        raise Exception ("param error")
#    _(STATE_VPS_TO_CLOSE, STATE_VPS_CLOSED, vps_close)



if "__main__" == __name__:
    main()

