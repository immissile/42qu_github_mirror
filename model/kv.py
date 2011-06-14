#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import mc, cursor_by_table
from zkit.ordereddict import OrderedDict

class Kv(object):
    def __init__(self, table, NULL=''):
        self.__table__ = table
        self.cursor = cursor_by_table(table)
        self.__mc_key__ = '%s.%%s'%table
        self.__mc_id__ = '-%s'%self.__mc_key__
        self.NULL = NULL

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
                r = self.NULL
            mc.set(mc_key, r)
        return r

    def iteritems(self):
        id = 0
        cursor = self.cursor
        while True:
            cursor.execute('select id,value from %s where id>%%s order by id limit 128'%self.__table__, id)
            result = cursor.fetchall()
            if not result:
                break
            for id, value in result:
                yield id, value
           

    def set(self, key, value):
        r = self.get(key)
        if r != value:
            mc_key = self.__mc_key__%key
            cursor = self.cursor
            table = self.__table__
            cursor.execute(
                'insert delayed into %s (id,value) values (%%s,%%s) on duplicate key update value=%%s'%table,
                (key, value, value)
            )
            cursor.connection.commit()
            mc.set(mc_key, value)

    def delete(self, key):
        cursor = self.cursor
        cursor.execute('delete from %s where id=%%s'%self.__table__, key)
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
        else:
            r = 0
        return r

    def mc_id_by_value(self, value):
        mc_key = self.__mc_id__
        mc_key = mc_key%value
        r = mc.get(mc_key)
        if r is None:
            r = self.id_by_value(value)
            mc.set(mc_key, r)
        return r


    def insert(self, value): 
        cursor = self.cursor
        cursor.execute(
            'insert into %s (value) values (%%s)'%self.__table__,
            value
        )
        cursor.connection.commit()
        r = cursor.lastrowid
        return r

    def id_by_value_new(self, value):
        return self.id_by_value(value) or self.insert(value)
    
    def mc_id_by_value_new(self, value):
        return self.mc_id_by_value(value) or self.insert(value)

    def value_by_id_list(self, id_list):
        mc_key = self.__mc_key__
        keydict = dict((i, mc_key%i) for i in id_list)
        mcdict = mc.get_dict(keydict.itervalues())
        r = OrderedDict()
        for i in id_list:
            value = mcdict.get(keydict[i])
            if value is None:
                value = self.get(i)
            r[i] = value
        return r


