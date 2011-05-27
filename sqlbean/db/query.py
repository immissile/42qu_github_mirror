#coding:utf-8
import sys

def escape(string):
    return '`%s`' % string

def conditions_null(kwargs, sql_conditions_str):
    kwds = {}
    for k, v in kwargs.iteritems():
        if v is None:
            sql_conditions_str.append("%s is NULL"%escape(k))
        else:
            kwds[k] = v
    return kwds

class Query(object):
    '''
    Gives quick access to database by setting attributes (query conditions, et
    cetera), or by the sql methods.

    Instance Methods
    ----------------

    Creating a Query object requires a Model class at the bare minimum. The
    doesn't run until results are pulled using a slice, ``list()`` or iterated
    over.

    For example::

        q = Query(model=MyModel)

    This sets up a basic query without conditions. We can set conditions using
    the ``where`` method::

        q.where(name='John', age=30)

    We can also chain the ``where`` method::

        q.where(name='John').where(age=30)

    In both cases the ``WHERE`` clause will become::

        WHERE `name` = 'John' AND `age` = 30

    You can also order using ``order_by`` to sort the results::

        # The second arg is optional and will default to ``ASC``
        q.order_by('column', 'DESC')

    You can limit result sets by slicing the Query instance as if it were a
    list. Query is smart enough to translate that into the proper ``LIMIT``
    clause when the query hasn't yet been run::

        q = Query(model=MyModel).where(name='John')[:10]   # LIMIT 0, 10
        q = Query(model=MyModel).where(name='John')[10:20] # LIMIT 10, 10
        q = Query(model=MyModel).where(name='John')[0]    # LIMIT 0, 1

    Simple iteration::

        for obj in Query(model=MyModel).where(name='John'):
            # Do something here

    Counting results is easy with the ``count`` method. If used on a ``Query``
    instance that has not yet retrieve results, it will perform a ``SELECT
    COUNT(*)`` instead of a ``SELECT *``. ``count`` returns an integer::

        count = Query(model=MyModel).where=(name='John').count()

    Class Methods
    -------------

    ``Query.raw_sql(sql, values)`` returns a database cursor. Usage::

        query = 'SELECT * FROM `users` WHERE id = ?'
        values = (1,) # values must be a tuple or list

        # Now we have the database cursor to use as we wish
        cursor = Query.raw_swl(query, values)

    ``Query.sql(sql, values)`` has the same syntax as ``Query.raw_sql``, but
    it returns a dictionary of the result, the field names being the keys.

    '''

    def __init__(self, query_type='SELECT *', args=(), conditions={}, model=None, db=None):
        #from sqlbean.model import Model
        self.type = query_type
        if args:
            self.sql_conditions_str = [args[0]]
            self.sql_conditions_para = list(args[1:])
        else:
            self.sql_conditions_str = []
            self.sql_conditions_para = []

        self.conditions = conditions_null(conditions, self.sql_conditions_str)

        self.order = ''
        self.limit = ()
        self.cache = None
        #if not issubclass(model, Model):
        #    raise Exception('Query objects must be created with a model class.')
        self.model = model
        if db:
            self.db = db
        elif model:
            self.db = model.db

    def __getitem__(self, k):
        if self.cache != None:
            return self.cache[k]

        if isinstance(k, (int, long)):
            self.limit = (k, 1)
            lst = self.get_data()
            if not lst:
                return None
            return lst[0]
        elif isinstance(k, slice):
            if k.start == 0 and  k.stop is None:
                self.limit = ()
            elif k.start is not None:
                assert k.stop is not None, "Limit must be set when an offset is present"
                assert k.stop >= k.start, "Limit must be greater than or equal to offset"
                self.limit = k.start, (k.stop - k.start)
            elif k.stop is not None:
                self.limit = 0, k.stop

        return self.get_data()

    def __len__(self):
        return len(self.get_data())

    def __iter__(self):
        return iter(self.get_data())

    def __repr__(self):
        return repr(self.get_data())

    def count(self, what='*'):
        if self.cache is None:
            result = Query.raw_sql(
                'SELECT COUNT(%s) FROM %s %s' % (
                    what,
                    self.model.Meta.table_safe,
                    self.extract_condition_keys() or ''
                ),
                self.extract_condition_values(),
                self.db
            )

            #奇怪,DBUtils不这样写返回的就是None
            result = result.fetchone()
            if result:
                result = result[0]
            else:
                result = 0
        else:
            result = len(self.cache)

        return result



    def where(self, *args, **kwargs):
        if args:
            self.sql_conditions_str.append(args[0])
            self.sql_conditions_para.extend(args[1:])
        kwds = conditions_null(kwargs, self.sql_conditions_str)
        self.conditions.update(kwds)

        return self

    def order_by(self, field):
        self.order = 'ORDER BY %s' % field
        return self

    def extract_condition_keys(self):
        if len(self.conditions) or len(self.sql_conditions_str):
            return 'WHERE %s' % ' AND '.join(
                ["%s=%%s" % escape(k) for k in self.conditions]+self.sql_conditions_str
            )

    def extract_condition_values(self):
        return list(self.conditions.itervalues())+self.sql_conditions_para

    def query_template(self):
        return '%s FROM %s %s %s %s' % (
            self.type,
            self.model.Meta.table_safe,
            self.extract_condition_keys() or '',
            self.order,
            self.extract_limit() or '',
        )

    def extract_limit(self):
        if len(self.limit):
            return 'LIMIT %s' % ', '.join(str(l) for l in self.limit)

    def get_data(self):
        if self.cache is None:
            self.cache = list(self.iterator())
        return self.cache

    def iterator(self):
        q = self.execute_query()
        q = q.fetchall()
        for row in q:
            obj = self.model(*row)
            obj._new_record = False
            yield obj

    def execute_query(self):
        values = self.extract_condition_values()
        return Query.raw_sql(self.query_template(), values, self.db)

    def update(self, *args, **kwds):
        values = self.extract_condition_values()
        update_set = []
        if args:
            update_set.append(args[0])
            values = args[1:]+values
        if kwds:
            update_set.append(
                ','.join(
                    "%s=%%s"%(
                        escape(k)
                    )
                    for k in kwds.keys()
                )
            )
            values = list(kwds.values())+values
        if update_set:
            Query.raw_sql(
                'UPDATE %s SET %s %s' % (
                    self.model.Meta.table_safe,
                    ','.join(update_set),
                    self.extract_condition_keys() or ''
                ),
                values,
                self.db
            )

    def delete(self):
        values = self.extract_condition_values()
        Query.raw_sql(
            'DELETE FROM %s %s' % (
                self.model.Meta.table_safe,
                self.extract_condition_keys() or ''
            ),
            values,
            self.db
        )

    @classmethod
    def get_db(cls, db=None):
        return db or cls.db

    @classmethod
    def cursor(cls, db=None):
        db = db or cls.get_db()
        cursor = db.cursor()
        return cursor

    @classmethod
    def sql(cls, sql, values=(), db=None):
        db = db or cls.get_db()
        cursor = Query.raw_sql(sql, values, db)
        fields = [f[0] for f in cursor.description]
        return [dict(zip(fields, row)) for row in cursor.fetchall()]

    @classmethod
    def raw_sql(cls, sql, values=(), db=None):
        db = db or cls.get_db()
        cursor = db.cursor()
        try:
            if values:
                cursor.execute(sql, values)
            else:
                cursor.execute(sql)
            if db.b_commit:
                cls.commit(db)
        except Exception, ex:
            print "sql:", sql
            print "values:", values
            print "raw_sql: exception: ", ex
            sys.stdout.flush()
            raise
        #print "sql:", sql
        #print "values:", values
        return cursor

    def id_list(self, limit=None, offset=None):
        self.type = "SELECT id"
        self.limit = _limit = []
        if limit is not None:
            if offset is not None:
                _limit.append(offset)
            _limit.append(limit)
        return [i[0] for i in self.execute_query()]

    @classmethod
    def raw_sqlscript(cls, sql, db=None):
        db = db or cls.get_db()
        cursor = db.cursor()
        try:
            cursor.executescript(sql)
            if db.b_commit:
                cls.commit(db)
        except BaseException, ex:
            print "raw_sqlscript: exception: ", ex
            print "sql:", sql
        return cursor



# begin() and commit() for SQL transaction control
# This has only been tested with SQLite3 with default isolation level.
# http://www.python.org/doc/2.5/lib/sqlite3-Controlling-Transactions.html

    @classmethod
    def begin(cls, db=None):
        """
        begin() and commit() let you explicitly specify an SQL transaction.
        Be sure to call commit() after you call begin().
        """
        db = db or cls.get_db()
        db.b_commit = False

    @classmethod
    def rollback(cls, db=None):
        db = db or cls.get_db()
        cursor = db.cursor()
        cursor.connection.rollback()


    @classmethod
    def commit(cls, db=None):
        """
        begin() and commit() let you explicitly specify an SQL transaction.
        Be sure to call commit() after you call begin().
        """
        cursor = db.cursor()
        try:
            db = db or cls.get_db()
            cursor.connection.commit()
        finally:
            db.b_commit = True
        return cursor
