#!/usr/bin/env python
# -*- coding: utf-8 -*-
from array import array
from hashlib import md5
from _db import mc, cursor_by_table
from zkit.ordereddict import OrderedDict


class Kv(object):
    def __init__(self, table, NULL=''):
        self.__table__ = table
        self.cursor = cursor_by_table(table)
        self.__mc_id__ = '%s.%%s' % table
        self.__mc_value__ = '-%s' % self.__mc_id__
        self.NULL = NULL


    def get(self, id):
        mc_key = self.__mc_id__ % id
        r = mc.get(mc_key)
        if r is None:
            cursor = self.cursor
            cursor.execute('select value from %s where id=%%s' % self.__table__, id)
            r = cursor.fetchone()
            if r:
                r = r[0]
            if r is None:
                r = self.NULL
            mc.set(mc_key, r)
        return r

    def get_dict(self, id_list):
        if type(id_list) not in (array, list, tuple, dict):
            id_list = tuple(id_list)
        mc_key = self.__mc_id__
        result = mc.get_dict([mc_key%i for i in id_list])
        r = {}
        for i in id_list:
            t = result.get(mc_key%i)
            if t is None:
                t = self.get(i)
            r[i] = t
        return r

    def get_list(self, id_list):
        if type(id_list) not in (array, list, tuple, dict):
            id_list = tuple(id_list)
        mc_key = self.__mc_id__
        result = mc.get_dict([mc_key%i for i in id_list])
        r = []
        for i in id_list:
            t = result.get(mc_key%i)
            if t is None:
                t = self.get(i)
            r.append(t)
        return r

    def iteritems(self):
        id = 0
        cursor = self.cursor
        while True:
            cursor.execute('select id,value from %s where id>%%s order by id limit 128' % self.__table__, id)
            result = cursor.fetchall()
            if not result:
                break
            for id, value in result:
                yield id, value

    def mc_value_id_set(self, value, id):
        h = md5(value).hexdigest()
        mc_key = self.__mc_value__ % h
        mc.set(mc_key, id)

    def set(self, id, value):
        r = self.get(id)
        if r != value:
            mc_key = self.__mc_id__ % id
            cursor = self.cursor
            table = self.__table__
            cursor.execute(
                'insert into %s (id,value) values (%%s,%%s) on duplicate key update value=values(value)' % table,
                (id, value)
            )
            cursor.connection.commit()
            if value is None:
                value = False
            mc.set(mc_key, value)

    def mc_flush(self, id):
        mc_key = self.__mc_id__ % id
        mc.delete(mc_key)

    def delete(self, id):
        cursor = self.cursor
        cursor.execute('delete from %s where id=%%s' % self.__table__, id)
        mc_key = self.__mc_id__ % id
        mc.delete(mc_key)

    def id_by_value(self, value):
        cursor = self.cursor
        cursor.execute(
            'select id from %s where value=%%s' % self.__table__,
            value
        )
        r = cursor.fetchone()
        if r:
            r = r[0]
        else:
            r = 0
        return r

    def mc_id_by_value(self, value):
        h = md5(value).hexdigest()
        mc_key = self.__mc_value__ % h
        r = mc.get(mc_key)
        if r is None:
            r = self.id_by_value(value)
            mc.set(mc_key, r)
        return r

    def insert_no_value_cache(self, value):
        cursor = self.cursor
        cursor.execute(
            'insert into %s (value) values (%%s)' % self.__table__,
            value
        )
        cursor.connection.commit()
        id = cursor.lastrowid
        mc_key = self.__mc_id__ % id
        mc.set(mc_key, value)
        return id

    def insert(self, value):
        id = self.insert_no_value_cache(value)
        self.mc_value_id_set(value, id)
        return id

    def id_by_value_new(self, value):
        return self.id_by_value(value) or self.insert(value)

    def mc_id_by_value_new(self, value):
        id = self.mc_id_by_value(value)
        if not id:
            id = self.insert(value)
            h = md5(value).hexdigest()
            mc_key = self.__mc_value__ % h
            mc.set(mc_key, id)
        return id

    def value_by_id_list(self, id_list):
        mc_key = self.__mc_id__
        keydict = dict((i, mc_key % i) for i in id_list)
        mcdict = mc.get_dict(keydict.itervalues())
        r = OrderedDict()
        for i in id_list:
            value = mcdict.get(keydict[i])
            if value is None:
                value = self.get(i)
            r[i] = value
        return r
