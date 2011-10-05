#coding:utf-8
from _db import McModel, McCache, cursor_by_table, McCacheA, McCacheM
from feed import PAGE_LIMIT, MAXINT
from model.site_po import po_id_list_by_zsite_id
from model.state import STATE_PO_ZSITE_SHOW_THEN_REVIEW

ID_SQL = 'select id from po where state>=%s and zsite_id=%%s and id<%%s order by id desc limit %s'%(
    STATE_PO_ZSITE_SHOW_THEN_REVIEW,
    PAGE_LIMIT
)

def site_po_id_lastest(id):
    return po_id_list_by_zsite_id(id, 0, PAGE_LIMIT, 0)

cursor = cursor_by_table('po') 

def feed_iter(zsite_id, start_id=MAXINT):
    if start_id == MAXINT:
        id_list = site_po_id_lastest(zsite_id)
        if id_list:
            for i in id_list:
                yield i
            start_id = i
        else:
            return
    while True:
        cursor.execute(ID_SQL, (zsite_id, start_id))
        c = cursor.fetchall()
        if not c:
            break
        for i in c:
            yield i
        start_id = i[0]


if __name__ == '__main__':
    for i in feed_iter(10099440):
        print i


        
