#coding:utf-8

from _db import cursor_by_table, McModel, McLimitA, McCache, McNum, Model, McCacheM

mc_pos_id_list_by_cid = McCacheM("PosIdListByCid:%s")


def po_id_list_by_zsite_id(zsite_id, ):
    pass


class ZsiteSiteMax(Model):
    pass

class ZsiteSitePos(Model):
    pass


def pos_id_list_by_cid(zsite_id , user_id):
    r = ZsiteSitePos.where(zsite_id=zsite_id, user_id=user_id).col_list(
            col='cid,pos_id'
        )
    return dict(r)

def pos_mark_all(zsite_id, user_id):
    pass

def pos_mark(zsite_id, user_id, cid):
    pass

def next_id_list(zsite_id, user_id):
    pass


if __name__ == "__main__":
    print pos_id_list_by_cid(1, 2)

