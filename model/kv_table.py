#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import mc,cursor_by_table

class KvTable(object):
    def __init__(self, table):
        self.__table__ = table
        self.cursor = cursor_by_table(table)
        self.__mc_key__ = "%s.%%s"%table

    def get(self, key):
        mc_key = self.__mc_key__%key
        r = mc.get(mc_key)
        if r is None:
            c = self.cursor.execute('select value from %s where id=%%s'%self.__tabel__, key)
            r = c.fetchone()
            if r:
                r = r[0]
            if r is None:
                r = False
            mc.set(mc_key, r)
        return r

    def set(self, key, value):
        r = self.get(key)
        if r != value:
            mc_key = self.__mc_key__%key
            cursor = self.cursor
            table = self.__tabel__
            if r is False:
                cursor.execute('insert delayed into %s (id,value) values (%%s,%%s)'%table, key, value)
            else:
                cursor.execute('update %s set value=%%s where id=%%s'%table, value, key)
            cursor.connection.commit()
            mc.set(key, value)

    def delete(key):
        cursor.execute("delete from %s where id=%%s"%self.__tabel__, key)
        mc.delete(key)

