#coding:utf-8

from _db import feed_cursor

def init_zsite(zsite_id): 
    feed_cursor.execute("""CREATE TABLE feed_%s (id INTEGER UNSIGNED NOT NULL,PRIMARY KEY (id)) ENGINE = MyISAM"""%zsite_id)

def init_user(user_id):
    init_zsite(user_id)

if __name__ == "__main__":
    init_user(2)
