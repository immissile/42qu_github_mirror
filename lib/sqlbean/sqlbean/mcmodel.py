#coding:utf-8
from sqlbean.db.query import Query, escape
from sqlbean.db.mc_connection import mc
from marshal import dumps, loads
from sqlbean.metamodel import cache, lower_name, ModelBase, get_or_create, save, get, __eq__, __ne__
from array import array
from datetime import datetime

def model_dumps(self):
    value = []
    for i in self._fields:
        v = self.__dict__.get(i, None)
        if type(v) is datetime:
            v = v.strftime("%Y-%m-%d %H:%M:%S")
        value.append(v)
    value = dumps(tuple(value))
    return value

class McModel(object):
    @classmethod
    def _loads(cls, value):
        value = loads(value)
        value = cls(*value)
        value._new_record = False
        return value

    __metaclass__ = ModelBase

    debug = False
    get_or_create = get_or_create
    __eq__ = __eq__
    __ne__ = __ne__

    def __init__(self, *args, **kwargs):
        'Allows setting of fields using kwargs'
        self.__dict__[self.Meta.pk] = None
        self._new_record = True
        for i, arg in enumerate(args):
            self.__dict__[self._fields[i]] = arg
        for i in self._fields[len(args):]:
            self.__dict__[i] = kwargs.get(i)
        self.__dict__["_changed"] = set()

    @classmethod
    def mc_get(cls, id):
        if id:
            key = cls.Meta.mc_key%id
            value = mc.get_marshal(key, cls._loads)
            if value is None:
                value = cls.get(id)
                if value:
                    value.mc_set()
            return value

    @classmethod
    def mc_flush_multi(cls, id_list):
        mc_key = cls.Meta.mc_key
        result = mc.get_multi_marshal([mc_key%i for i in id_list], cls._loads)
        return result

    @classmethod
    def mc_get_multi(cls, id_list):
        if type(id_list) not in (array, list, tuple, dict):
            id_list = tuple(id_list)
        mc_key = cls.Meta.mc_key
        result = mc.get_multi_marshal([mc_key%i for i in id_list], cls._loads)
        r = {}
        for i in id_list:
            t = result.get(mc_key%i)
            if t is None:
                t = cls.get(i)
                if t:
                    t.mc_set()
            r[i] = t
        return r

    @classmethod
    def mc_get_list(cls, id_list):
        id_list = tuple(id_list)
        mc_key = cls.Meta.mc_key
        result = mc.get_multi_marshal([mc_key%i for i in id_list], cls._loads)
        r = []
        for i in id_list:
            t = result.get(mc_key%i)
            if t is None:
                t = cls.get(i)
                if t:
                    t.mc_set()
            r.append(t)

        return r


    @classmethod
    def mc_delete(cls, id):
        mc.delete(cls.Meta.mc_key%id)

    def mc_flush(self):
        mc.delete(self.Meta.mc_key%self.id)

    def mc_set(self):
        key = self.Meta.mc_key%self.id
        mc.set_marshal(key, self, dumps=model_dumps)

    def __setattr__(self, name, value):
        'Records when fields have changed'
        dc = self.__dict__
        if name[0] != "_":
            fields = self._fields
            if name in fields:
                dc_value = dc[name]
                if dc_value is None:
                    self._changed.add(name)
                else:
                    if value is not None:
                        value = type(dc_value)(value)
                    if dc_value != value:
                        self._changed.add(name)
        dc[name] = value

    def _get_pk(self):
        'Returns value of primary key'
        return getattr(self, self.Meta.pk)

    def _get_pk(self):
        'Sets the current value of the primary key'
        return getattr(self, self.Meta.pk, None)

    def _set_pk(self, value):
        'Sets the primary key'
        return setattr(self, self.Meta.pk, value)

    def _update(self):
        if not self._changed:return
        'Uses SQL UPDATE to update record'
        query = 'UPDATE %s SET ' % self.Meta.table_safe
        query += ','.join(['%s=%%s' % escape(f) for f in self._changed])
        query += ' WHERE %s=%%s ' % (escape(self.Meta.pk))

        values = [getattr(self, f) for f in self._changed]
        values.append(self._get_pk())

        cursor = Query.raw_sql(query, values, self.db)
        self.mc_set()

    def _new_save(self):
        'Uses SQL INSERT to create new record'
        # if pk field is set, we want to insert it too
        # if pk field is None, we want to auto-create it from lastrowid
        auto_pk = 1 and (self._get_pk() is None) or 0
        fields = [
            f for f in self._fields
            if f != self.Meta.pk or not auto_pk
        ]

        used_fields = []
        values = []
        for i in fields:
            v = getattr(self, i, None)
            if v is not None:
                used_fields.append(escape(i))
                values.append(v)
        query = 'INSERT INTO %s (%s) VALUES (%s)' % (self.Meta.table_safe,
                ', '.join(used_fields),
                ', '.join(["%s"] * len(used_fields))
        )
        cursor = Query.raw_sql(query, values, self.db)


        if self._get_pk() is None:
            self._set_pk(cursor.lastrowid)
        return True

    def _set_default(self):
        if hasattr(self.Meta, 'default'):
            default = self.Meta.default
            i = default()

            for k, v in default.__dict__.iteritems():
                if k[0] != '_' :
                    if getattr(self, k, None) is None:
                        if callable(v):
                            v = getattr(i, k)()
                        setattr(self, k, v)


    @classmethod
    def raw_sql(cls, query, *args):
        result = Query.raw_sql(query, args, cls.db)
        return result

    def delete(self):
        'Deletes record from database'
        query = 'DELETE FROM %s WHERE `%s` = %%s' % (self.Meta.table_safe, self.Meta.pk)
        values = [getattr(self, self.Meta.pk)]
        Query.raw_sql(query, values, self.db)
        self.mc_flush()

    def update(self, **kwds):
        set_what = ','.join(
            "%s=%%s"%(
                escape(k)
            )
            for k in kwds.keys()
        )
        query = 'UPDATE %s SET %s WHERE `%s` = %%s' % (
            self.Meta.table_safe,
            set_what, self.Meta.pk
        )
        values = kwds.values()+[getattr(self, self.Meta.pk)]
        Query.raw_sql(query, values, self.db)


    @classmethod
    def where(cls, *args, **kwargs):
        'Returns Query object'
        return Query(
            model=cls,
            args=args,
            conditions=kwargs
        )

    get = get

    @classmethod
    def count(cls, *args, **kwargs):
        return Query(
            model=cls,
            args=args,
            conditions=kwargs
        ).count(1)


    @classmethod
    def begin(cls):
        """
        begin() and commit() let you explicitly specify an SQL transaction.
        Be sure to call commit() after you call begin().
        """
        db = cls.db
        db.b_commit = False

    @classmethod
    def commit(cls):
        db = cls.db
        try:
            cursor = db.cursor()
            cursor.connection.commit()
        finally:
            db.b_commit = True

    @classmethod
    def rollback(cls, db=None):
        db = cls.db
        try:
            cursor = db.cursor()
            cursor.connection.rollback()
        finally:
            db.b_commit = True

    save = save

    @classmethod
    def replace_into(cls, **kwds):
        pk = cls.Meta.pk
        if pk in kwds:
            id = kwds[pk]
            ins = cls.mc_get(id)
            if ins is None:
                ins = cls(id=id)
            del kwds[pk]
        else:
            ins = cls()

        for k, v in kwds.iteritems():
            setattr(ins, k, v)
        ins.save()

        return ins

    @classmethod
    def mc_bind(cls, xxx_list, property, key="id"):
        d = []
        e = []
        for i in xxx_list:
            k = getattr(i, key)
            if k:
                d.append(k)
                e.append((k, i))
            else:
                i.__dict__[property] = None

        r = cls.mc_get_multi(set(d))
        for k, v in e:
            v.__dict__[property] = r.get(k)



