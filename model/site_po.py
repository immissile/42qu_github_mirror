#coding:utf-8

from _db import cursor_by_table, McModel, McLimitA, McCache, McNum
#from import 

class ZsiteSiteMax(Model):
    pass

class ZsiteSitePos(Model):
    pass


def pos_id_list_by_cid(zsite_id , user_id):
    return ZsiteSitePos.where(zsite_id=zsite_id)

def pos_mark(zsite_id):
    pass

def next_id_list(zsite_id, user_id):
    pass


if __name__ == "__main__":
    pass


