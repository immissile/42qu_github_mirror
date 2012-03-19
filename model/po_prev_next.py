#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import McModel, McCache, McNum, McCacheA
from zsite_tag import ZsiteTagPo
from model.state import STATE_PO_ZSITE_SHOW_THEN_REVIEW
from model.cid import CID_EVENT_NOTICE
from model.po import Po

mc_po_prev_next = McCacheA('PoPrevNext:%s')
mc_site_po_prev_next = McCacheA('SitePoPrevNext:%s')

def mc_flush(po, zsite_id, zsite_tag_id=0):
    cid = po.cid
    po_id = po.id
    if zsite_tag_id:
        key = '%s_%s_%s_'%(cid, zsite_id, zsite_tag_id)
        mc_po_prev_next.delete('%s%s'%(key, po_id))
        prev_po_id, next_po_id = po_prev_next(po, zsite_tag_id)
        mc_po_prev_next.delete('%s%s'%(key, prev_po_id))
        mc_po_prev_next.delete('%s%s'%(key, next_po_id))
    elif po.zsite_id == po.user_id:
        mc_site_po_prev_next.delete(po_id)
        for i in site_po_prev_next(zsite_id, po_id):
            if i:
                mc_site_po_prev_next.delete(i)

def po_prev_next(po, zsite_tag_id):
    cid = po.cid
    po_id = po.id
    zsite_id = po.user_id

    if zsite_tag_id:
        return _po_prev_next(cid, zsite_id, zsite_tag_id, po_id)
    elif cid == CID_EVENT_NOTICE:
        pass
    elif po.zsite_id == po.user_id:
        return site_po_prev_next(zsite_id, po_id)
    return None, None


@mc_site_po_prev_next('{po_id}')
def site_po_prev_next(site_id, po_id):
    def _site_po_goto(sql):
        c = Po.raw_sql(
            sql,
            site_id,
            site_id,
            po_id,
            STATE_PO_ZSITE_SHOW_THEN_REVIEW,
        ).fetchone()
        return c[0] if c is not None else 0

    def _site_po_goto_direct(sql):
        c = Po.raw_sql(
            sql,
            site_id,
            site_id,
            STATE_PO_ZSITE_SHOW_THEN_REVIEW,
        ).fetchone()
        return c[0] if c is not None else 0

    _prev = _site_po_goto( 'select id from po where user_id=%s and zsite_id=%s and id>%s and state>=%s order by id limit 1')

    _next = _site_po_goto( 'select id from po where user_id=%s and zsite_id=%s and id<%s and state>=%s order by id desc limit 1')

    if _prev != _next:
        if not _prev:
            _prev = _site_po_goto_direct('select id from po where user_id=%s and zsite_id=%s and state>=%s order by id limit 1')
        elif not _next:
            _next = _site_po_goto_direct('select id from po where user_id=%s and zsite_id=%s and state>=%s order by id desc limit 1')

    return [_prev, _next]

@mc_po_prev_next('{cid}_{zsite_id}_{zsite_tag_id}_{po_id}')
def _po_prev_next(cid, zsite_id, zsite_tag_id, po_id):
    t = ZsiteTagPo.get(zsite_id=zsite_id, po_id=po_id, zsite_tag_id=zsite_tag_id)
    if not t:
        result = (0, 0)
    else:
        id = t.id
        result = [
            _po_goto(
                'select po_id from zsite_tag_po where cid=%s and zsite_id=%s and zsite_tag_id=%s and id>%s order by id limit 1',
                cid,
                zsite_id,
                zsite_tag_id,
                id,
            ) or 0
            ,
            _po_goto(
                'select po_id from zsite_tag_po where cid=%s and zsite_id=%s and zsite_tag_id=%s and id<%s order by id desc limit 1',
                cid,
                zsite_id,
                zsite_tag_id,
                id,
            ) or 0
        ]

    if result[0] != result[1]:
        if not result[0]:
            c = ZsiteTagPo.raw_sql(
                'select po_id from zsite_tag_po where cid=%s and zsite_id=%s and zsite_tag_id=%s order by id limit 1',
                cid,
                zsite_id,
                zsite_tag_id,
            )
            result[0] = c.fetchone()[0]
        elif not result[1]:
            c = ZsiteTagPo.raw_sql(
                'select po_id from zsite_tag_po where cid=%s and zsite_id=%s and zsite_tag_id=%s order by id desc limit 1',
                cid,
                zsite_id,
                zsite_tag_id,
            )
            result[1] = c.fetchone()[0]

    return result


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
    from model.po import Po

    po = Po.mc_get(10101228)
    print po.name
    from model.zsite_tag import zsite_tag_id_tag_name_by_po_id
    zsite_tag_id, tag_name = zsite_tag_id_tag_name_by_po_id(po.user_id, po.id)
    print zsite_tag_id, tag_name
    print po_prev_next(po, zsite_tag_id)

