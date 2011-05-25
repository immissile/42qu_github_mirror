from sqlbean.db.use_sqlite import use_sqlite

database = use_sqlite("test.sqlite")

from sqlbean.shortcut import Model

def init_table():
    c = database.cursor()
    try:
        c.execute("""
        CREATE TABLE user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name CHAR(255)
        ) 
        """)
    except:
        pass
    c.execute("""
    insert into user (name) values ("zsp");
    """)
    c.connection.commit()

init_table()

class User(Model):
    pass

for i in User.where():
    print i.id, i.name

print User.where(id=1)