#coding:utf-8
from os.path import join, abspath, dirname, exists
from os import makedirs
from kyotocabinet import DB

class KvDb(object):
    def __init__(self, path=join(dirname(abspath(__file__)), "db")):
        self.path = path
        self.opendb = []

        if not exists(path):
            makedirs(path)

    def open_db(self, name):
        db = DB()
        db.open(
            join(self.path, "%s.kch"name),
            DB.OWRITER | DB.OCREATE
        )
        self.opendb.append(db)
        return db

    def close_db(self, name):
        for i in self.opendb:
            i.close()

if __name__ == "__main__":

    kvdb = KvDb()
    fetch_cache = kvdb.open_db( "fetch_uid")
    for i in fetch_cache:
        print i, fetch_cache[i]

