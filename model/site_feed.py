#coding:utf-8
from _db import McModel, McCache, cursor_by_table, McCacheM
from feed import PAGE_LIMIT
from model.site_po import po_id_list_by_zsite_id
from model.state import STATE_PO_ZSITE_SHOW_THEN_REVIEW
from zkit.feed_merge import MAXINT, merge_iter as _merge_iter
from model.zsite import Zsite
from model.po import Po
from model.ico import ico_url_bind_with_default
from model.cid import CID_WORD

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
                #print zsite_id, i
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
            #print zsite_id, i
            yield i[0]
        start_id = i[0]


def merge_iter(
    id_list, limit=MAXINT, begin_id=MAXINT
):
    return _merge_iter(
        feed_iter, id_list, limit, begin_id
    )

def site_po_iter(id_list, limit=MAXINT, begin_id=MAXINT):
    id_list = list(merge_iter(id_list, limit, begin_id))
    po_list = Po.mc_get_list(id_list)

    zsite_set = set()

    for i in po_list:
        zsite_set.add(i.zsite_id)
        zsite_set.add(i.user_id)

    zsite_dict = Zsite.mc_get_dict(zsite_set)

    result = []
    pre_zsite_id = None
    m = []

    zsite_set = set()

    if po_list:
        last_id = po_list[-1].id
        for i in po_list:
            if pre_zsite_id != i.zsite_id:
                if pre_zsite_id:
                    result.append([pre_zsite_id, m])
                    zsite_set.add(zsite_dict[pre_zsite_id])
                    m = []
                pre_zsite_id = i.zsite_id

            cid = i.cid
            t = []
            t.append(i.id)
            t.append(cid)

            if cid == CID_WORD:
                t.append(i.htm)
            else:
                t.append(i.name)

            if i.zsite_id != i.user_id:
                user = zsite_dict[i.user_id]
                t.append(user.link)
                t.append(user.name)
            m.append(t)

        result.append([i.zsite_id, m])
        zsite_set.add(zsite_dict[i.zsite_id])
    else:
        last_id = 0

    ico_url_bind_with_default(zsite_set)

    for i in result:
        id = i[0]
        zsite = zsite_dict[id]
        i[0] = [id, zsite.name, zsite.link, zsite.ico]

    return result, last_id


if __name__ == '__main__':
    for i in site_po_iter([10099440, 10092249]):
        print '*'*30
        for k in i[0]:
            print k,
        print ''
        for k in i[1]:
            print '\t',
            for j in k:
                print j,
            print ''
        print ''


