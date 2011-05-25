import MySQLdb
from DBUtils.PersistentDB import PersistentDB
persist = PersistentDB(MySQLdb,
    db='mokodb',
    host="localhost",
    user="root",
    passwd="111111",
)

DATABASE = persist.connection()

DATABASE.b_commit = True


def get_db_by_table(table_name):
    return DATABASE



from sqlbean.db import connection
connection.get_db_by_table = get_db_by_table

from sqlbean.shortcut import Model

class User(Model):
    class Meta:
        pk = "UserId"

for i in User.where():
    print i.UserId



