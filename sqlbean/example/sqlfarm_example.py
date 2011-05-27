from sqlbean.db.sqlstore import SqlStore

DATABASE_CONFIG = {
    "mokodb": {
    "master": "localhost:3306:mokodb:root:111111",
    "tables": ["*", "user"],
    },
}

SQLSTORE = SqlStore(db_config=DATABASE_CONFIG, **{})


def get_db_by_table(table_name):
    return SQLSTORE.get_db_by_table(table_name)


from sqlbean.db import connection
connection.get_db_by_table = get_db_by_table

from sqlbean.shortcut import Model

class User(Model):
    pass

for i in User.where():
    print i.id



