#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import cursor_by_table, McModel, McLimitA, McCache, McNum, McCacheA
from zsite_tag import ZsiteTagPo
from model.po import STATE_SECRET, STATE_ACTIVE

mc_po_prev_next = McCacheA("PoPrevNext:%s")


@mc_po_prev_next("{cid}_{zsite_id}_{tag_id}_{po_id}")
def po_prev_next(cid, zsite_id, tag_id,  po_id):
    t = ZsiteTagPo.get(zsite_id=zsite_id, po_id=po_id, zsite_tag_id=tag_id)
    if not t:
        result = (0, 0)
    else:
        id = t.id 
        result = [
            _po_goto(
                'select po_id from zsite_tag_po where cid=%s and zsite_id=%s and zsite_tag_id=%s and id>%s order by id limit 1',
                cid,
                zsite_id,
                tag_id,
                id,
            ) or 0
            ,
            _po_goto(
                'select po_id from zsite_tag_po where cid=%s and zsite_id=%s and zsite_tag_id=%s and id<%s order by id desc limit 1',
                cid,
                zsite_id,
                tag_id,
                id,
            ) or 0
        ]
   
    if result[0] != result[1]:
        if not result[0]:
            c = ZsiteTagPo.raw_sql(
                'select po_id from zsite_tag_po where cid=%s and zsite_id=%s and zsite_tag_id=%s order by id limit 1',
                cid,
                zsite_id,
                tag_id,
            )
            result[0] = c.fetchone()[0] 
        elif not result[1]:
            c = ZsiteTagPo.raw_sql(
                'select po_id from zsite_tag_po where cid=%s and zsite_id=%s and zsite_tag_id=%s order by id desc limit 1',
                cid,
                zsite_id,
                tag_id,
            )
            result[1] = c.fetchone()[0]
    
    return result



def mc_flush(cid, zsite_id, zsite_tag_id, id, po_id):
    _mc_flush(
        "select po_id from zsite_tag_po where zsite_id=%s and zsite_tag_id=%s and id>%s and cid=%s order by id limit 1",
        cid,
        zsite_id,
        zsite_tag_id,
        id,
    )
    _mc_flush( 
        "select po_id from zsite_tag_po where zsite_id=%s and zsite_tag_id=%s and id<%s and cid=%s order by id desc limit 1",
        cid,
        zsite_id,
        zsite_tag_id,
        id,
    )
    mc_po_prev_next.delete(
        "%s_%s_%s_%s_%s"%( cid, zsite_id, zsite_tag_id, po_id)
    )


def _mc_flush(sql, cid, zsite_id, zsite_tag_id, id):
    c = ZsiteTagPo.raw_sql(
        sql,
        zsite_id,
        zsite_tag_id,
        id,
        cid,
    )
    r = c.fetchone()
    if r:
        mc_po_prev_next.delete("%s_%s_%s"%(zsite_id, r[0], zsite_tag_id))



def _po_goto(
    sql,
    cid,
    zsite_id,
    tag_id,
    id,
):
    c = ZsiteTagPo.raw_sql(
        sql,
        cid,
        zsite_id,
        tag_id,
        id,
    )
    r = c.fetchone()
    if r:
        r = r[0]
    return r

if __name__ == '__main__':
    pass


