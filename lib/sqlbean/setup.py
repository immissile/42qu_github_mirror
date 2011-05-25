from setuptools import setup, find_packages

version = '0.601'

setup(name="sqlbean",
        version=version,
        description="A auto maping ORM for MYSQL and can bind with memcached",
        long_description=""" 


from sqlbean.db.sqlstore import SqlStore

#tables can in different databases

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

# will auto mapping the table structure
# class User will mapping to user
# class UserProfile will mapping to user_profile and so on 

class User(Model):
    pass

for i in User.where():
    print i.id


# more useage please the source code  :)


""",
        author="zsp",
        author_email="zsp007@gmail.com",
        packages=find_packages(),
        install_requires=['dbutils', 'decorator'],
        zip_safe=False
)
