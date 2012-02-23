#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from model._db import cursor_by_table

cursor = cursor_by_table('vps')

def main():
    cursor.execute("select id, state, ssh_port, `group` from vps")
    print cursor.fetchall()



if "__main__" == __name__:
    main()

