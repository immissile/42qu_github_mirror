#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import mc, cursor_by_table

class KvTable(object):
    def __init__(self, table):
        self.__table__ = table
        self.cursor = cursor_by_table(table)
        self.__mc_key__ = "%s.%%s"%table

    def get(self, key):
        mc_key = self.__mc_key__%key
        r = mc.get(mc_key)
        if r is None:
            cursor = self.cursor
            cursor.execute('select value from %s where id=%%s'%self.__table__, key)
            r = cursor.fetchone()
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
            table = self.__table__
            cursor.execute(
                'insert delayed into %s (id,value) values (%%s,%%s) on duplicate key update value=%%s'%table, (key, value, value)
            )
            cursor.connection.commit()
            mc.set(mc_key, value)

    def delete(self, key):
        cursor.execute("delete from %s where id=%%s"%self.__table__, key)
        mc_key = self.__mc_key__%key
        mc.delete(mc_key)

    def id_by_value(self, value):
        cursor = self.cursor
        cursor.execute(
            'select id from %s where value=%%s'%(self.__table__),
            value
        )
        r = cursor.fetchone()
        if r:
            r = r[0]
        return r

    def id_by_value_new(self, value):
        r = self.id_by_value(value)
        if r is None:
            cursor = self.cursor
            cursor.execute(
                "insert into %s (value) values (%%s)"%self.__table__,
                value
            )
            cursor.connection.commit()
            r = cursor.lastrowid
        return r




