#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import cursor_by_table

cursor = cursor_by_table('gid')

def gid():
    cursor.execute('insert into gid () values()')
    cursor.connection.commit()
    return cursor.lastrowid

if __name__ == '__main__':
    print gid()
