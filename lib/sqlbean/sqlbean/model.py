#coding:utf-8
from sqlbean.db.query import Query, escape
from sqlbean.metamodel import cache, lower_name, ModelBase, get_or_create, save, get , __eq__, __ne__

class Model(object):
    '''
    Allows for automatic attributes based on table columns.
    
    Syntax::
    
        from sqlbean.model import Model
        class MyModel(Model):
            class Meta:
                # If field is blank, this sets a default value on save
                class default:
                    field = 1
            
                # Table name is lower-case model name by default
                # Or we can set the table name
                table = 'mytable'
        
        # Create new instance using args based on the order of columns
        m = MyModel(1, 'A string')
        
        # Or using kwargs
        m = MyModel(field=1, text='A string')
        
        # Saving inserts into the database (assuming it validates [see below])
        m.save()
        
        # Updating attributes
        m.field = 123
        
        # Updates database record
        m.save()
        
        # Deleting removes from the database 
        m.delete()
        
        m = MyModel(field=0)
        
        m.save()
        
        # Retrieval is simple using Model.get
        # Returns a Query object that can be sliced
        MyModel.get(id)
        
        # Returns a MyModel object with an id of 7
        m = MyModel.get(7)
        
        # Limits the query results using SQL's LIMIT clause
        # Returns a list of MyModel objects
        m = MyModel.where()[:5]   # LIMIT 0, 5
        m = MyModel.where()[10:15] # LIMIT 10, 5
        
        # We can get all objects by slicing, using list, or iterating
        m = MyModel.get()[:]
        m = list(MyModel.where(name="zsp").where("age<%s",18))
        for m in MyModel.where():
            # do something here...
            
        # We can where our Query
        m = MyModel.where(field=1)
        m = m.where(another_field=2)
        
        # This is the same as
        m = MyModel.where(field=1, another_field=2)
        
        # Set the order by clause
        m = MyModel.where(field=1).order_by('-field')
        # Removing the second argument defaults the order to ASC
        
    '''
    __metaclass__ = ModelBase
    __eq__ = __eq__
    __ne__ = __ne__
    debug = False

    def __init__(self, *args, **kwargs):
        'Allows setting of fields using kwargs'
        self.__dict__[self.Meta.pk] = None
        self._new_record = True
        for i, arg in enumerate(args):
            self.__dict__[self._fields[i]] = arg
        for i in self._fields[len(args):]:
            self.__dict__[i] = kwargs.get(i)
        self.__dict__["_changed"] = set()

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

    save = save

    def _new_save(self):
        'Uses SQL INSERT to create new record'
        # if pk field is set, we want to insert it too
        # if pk field is None, we want to auto-create it from lastrowid
        pk = self._get_pk()
        auto_pk = 1 and (pk is None) or 0
        fields = [
            f for f in self._fields
            if f != self.Meta.pk or not auto_pk
        ]

        used_fields = []
        values = []
        for i in fields:
            v = getattr(self, i, None)
            #print i,v
            if v is not None:
                used_fields.append(escape(i))
                values.append(v)
        query = 'INSERT INTO %s (%s) VALUES (%s)' % (self.Meta.table_safe,
                ', '.join(used_fields),
                ', '.join(["%s"] * len(used_fields))
        )
        cursor = Query.raw_sql(query, values, self.db)



        if pk is None:
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

    get = get
    get_or_create = get_or_create

    @classmethod
    def replace_into(cls, **kwds):
        pk = cls.Meta.pk
        if pk in kwds:
            id = kwds[pk]
            ins = cls.get(id)
            if ins is None:
                ins = cls(id=id)
            del kwds[pk]
        else:
            ins = cls()

        for k, v in kwds.iteritems():
            setattr(ins, k, v)
        ins.save()

        return ins
