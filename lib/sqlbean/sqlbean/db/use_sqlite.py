import sqlite3



class Cursor(object):
    def __init__(self, cursor):
        self._cursor = cursor

    def __getattr__(self, name):
        return getattr(self._cursor, name)

    def execute(self, sql, *arg, **kwds):
        sql = sql.replace("%s", "?")
        return self._cursor.execute(sql, *arg, **kwds)

class Database(object):
    def __init__(self, db):
        self.db = db
        self.b_commit = True

    def __getattr__(self, name):
        return getattr(self.db, name)

    def cursor(self):
        cursor = self.db.cursor()
        return Cursor(cursor)

def use_sqlite(*args, **kwds):
    _DATABASE = sqlite3.connect(*args, **kwds)
    DATABASE = Database(_DATABASE)
    def get_db_by_table(table_name):
        return DATABASE

    from sqlbean.db import connection
    connection.get_db_by_table = get_db_by_table
    return DATABASE

