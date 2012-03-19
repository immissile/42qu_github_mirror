#!/usr/bin/env python
# -*- coding: utf-8 -*-
from zrank import hot, confidence
from _db import Model, McModel, McCache, McLimitA, McNum
from vote import vote_up_count, vote_down_count
from model.po import Po

ORDER = ('id', 'hot', 'confidence')

class Rank(McModel):
    pass

mc_rank_po_id_count = McCache('RankPoIdCount.%s')

@mc_rank_po_id_count('{to_id}_{cid}')
def rank_po_id_count(to_id, cid):
    qs = Rank.where(to_id=to_id)
    if int(cid):
        qs = qs.where(cid=cid)
    return qs.count()


mc_rank_po_id_list = McLimitA('RankPoIdList.%s', 512)

@mc_rank_po_id_list('{to_id}_{cid}_{order}')
def rank_po_id_list(to_id, cid, order, limit=512, offset=0):
    qs = Rank.where(to_id=to_id)
    if int(cid):
        qs = qs.where(cid=cid)
    return qs.order_by('%s desc' % order).col_list(limit, offset, 'po_id')


#mc_rank_to_id_by_po_id_cid = McCache('RankToIdByPoIdCid.%s')
#
#@mc_rank_to_id_by_po_id_cid('{po_id}_{cid}')
#def rank_to_id_by_po_id_cid(po_id, cid):
#    for to_id in Rank.where(po_id=po_id, cid=cid).col_list(1, 0, 'to_id'):
#        return to_id
#    return 0

mc_rank_id_by_po_id_to_id = McCache('RankIdByPoIdToId.%s')

@mc_rank_id_by_po_id_to_id('{po_id}_{to_id}')
def rank_id_by_po_id_to_id(po_id, to_id):
    r = Rank.get(po_id=po_id, to_id=to_id)
    if r:
        return r.id
    return 0

def rank_new(po, to_id, cid):
    po_id = po.id
    r = Rank(po_id=po_id, from_id=po.user_id, to_id=to_id, cid=cid)
    up = vote_up_count(po_id)
    down = vote_down_count(po_id)
    r.hot = hot(up, down, po.create_time)
    r.confidence = confidence(up, down)
    r.save()
    mc_flush_cid(to_id, cid)
    mc_rank_id_by_po_id_to_id.set('%s_%s' % (po_id, to_id), r.id)
#    mc_rank_to_id_by_po_id_cid.set('%s_%s' % (po_id, cid), to_id)
    return r

def rank_update(po_id):
    up = vote_up_count(po_id)
    down = vote_down_count(po_id)
    po = Po.mc_get(po_id)
    _hot = hot(up, down, po.create_time)
    _confidence = confidence(up, down)
    for r in Rank.where(po_id=po_id):
        r.hot = _hot
        r.confidence = _confidence
        r.save()
        mc_flush_cid(r.to_id, r.cid)

def rank_rm_all(po_id):
    for r in Rank.where(po_id=po_id):
        r.delete()
        mc_flush_cid(r.to_id, r.cid)
        mc_rank_id_by_po_id_to_id.set('%s_%s' % (po_id, r.to_id), 0)

def rank_rm(po_id, to_id):
    for r in Rank.where(po_id=po_id, to_id=to_id):
        r.delete()
        mc_flush_cid(to_id, r.cid)
    mc_rank_id_by_po_id_to_id.set('%s_%s' % (po_id, to_id), 0)

def _rank_mv(r, cid):
    o_cid = r.cid
    to_id = r.to_id
    if o_cid != cid:
        r.cid = cid
        r.save()
        _mc_flush_cid(to_id, o_cid)
        _mc_flush_cid(to_id, cid)

def rank_mv(po_id, to_id, cid):
    id = rank_id_by_po_id_to_id(po_id, to_id)
    r = Rank.mc_get(id)
    if r:
        _rank_mv(r, cid)

def _mc_flush_cid(to_id, cid):
    for order in ORDER:
        mc_rank_po_id_list.delete('%s_%s_%s' % (to_id, cid, order))
    mc_rank_po_id_count.delete('%s_%s' % (to_id, cid))

def mc_flush_cid(to_id, cid):
    for i in set([0, cid]):
        _mc_flush_cid(to_id, i)

if __name__ == '__main__':
    pass

    print mc_rank_po_id_list.count()
################################################################################
#mc_rid_list_by_po_id = McCacheA('RIdListByPoId:%s')
#
#@mc_rid_list_by_po_id('{po_id}')
#def rid_list_by_po_id(po_id):
#    return Rank.where(po_id=po_id).col_list(col='rid')
#
#def zsite_list_by_po_id(po_id):
#    ids = zsite_id_list_by_po_id(po_id)
#    return Zsite.mc_get_list(ids)
#
##TODO 日记分类tag实现
#def team_note_new(man_id, zsite_id, cid, title, txt, repaste=None):
#    subject_state = NOTE_SUBJECT_STATE_FAV if repaste else NOTE_SUBJECT_STATE_REVIEW
#    subject_id = man_note_subject_id_state(man_id, subject_state).id
#    note = note_new(man_id, title, txt, subject_id)
#    note_id = note.id
#
#    return _team_note_new(note_id, zsite_id, cid)
#
#def _team_note_new(note_id, zsite_id, cid):
#    note = Note.mc_get(note_id)
#
#    team_note_fav_new(note_id, zsite_id)
#
#    t = TeamNote(id=note_id, zsite_id=zsite_id, cid=cid)
#    up, down = note_rate_tuple(note_id)
#    t.hot = hot(up, down, note.create_time)
#    t.confidence = confidence(up, down)
#    t.save()
#    mc_zsite_id_by_note_id.set(note_id, zsite_id)
#    mc_flush(zsite_id, cid)
#    return t
#
#def team_note_fav_new(note_id, zsite_id):
#    id = feed_new_id(FEED_CID_NOTE_FAV, zsite_id)
#    NoteFav.raw_sql('insert into note_fav (id, man_id, rid, reply_id) values (%s, %s, %s, null)', id, zsite_id, note_id)
#
#def team_note_mv(note_id, cid):
#    n = TeamNote.mc_get(note_id)
#    if n:
#        o_cid = n.cid
#        if o_cid != cid and cid in CID_ID_STR_TUPLE[1:]:
#            cid = int(cid)
#            n.cid = cid
#            n.save()
#            zsite_id = n.zsite_id
#            mc_flush_cid(zsite_id, o_cid)
#            mc_flush_cid(zsite_id, cid)
#
#def team_note_rm(note_id):
#    n = TeamNote.mc_get(note_id)
#    if n:
#        zsite_id = n.zsite_id
#        team_note_fav_rm(note_id, zsite_id)
#        n.delete()
#        mc_zsite_id_by_note_id.set(note_id, 0)
#        mc_flush(zsite_id, n.cid)
#
#def team_note_fav_rm(note_id, zsite_id):
#    for i in NoteFav.where(man_id=zsite_id, rid=note_id):
#        feed_rm(i.id)
#        i.delete()
#
#def team_note_rank(note_id):
#    n = Note.mc_get(note_id)
#    if n:
#        t = TeamNote.mc_get(note_id)
#        if t:
#            up, down = note_rate_tuple(note_id)
#            t.hot = hot(up, down, n.create_time)
#            t.confidence = confidence(up, down)
#            t.save()
#            mc_flush(t.zsite_id, t.cid)
#
#ID_CACHE_LIMIT = 256
#
#mc_team_note_id_list = McLimitA('TeamNoteIdList.%s', ID_CACHE_LIMIT)
#
#@mc_team_note_id_list('{zsite_id}_{cid}_{order}')
#def team_note_id_list(zsite_id, cid, order, offset, limit):
#    qs = TeamNote.where(zsite_id=zsite_id)
#    if cid:
#        qs = qs.where(cid=cid)
#    order = ORDER_DIC[order]
#    return qs.order_by('%s desc' % order).col_list(limit, offset)
#
#def team_note_list(zsite_id, cid, order, offset=0, limit=3):
#    ids = team_note_id_list(zsite_id, cid, order, offset, limit)
#    return Note.mc_get_list(ids)
#
#def _team_note_total_by_cid(cid, title):
#    if cid:
#        return McNum(lambda zsite_id: TeamNote.where(zsite_id=zsite_id, cid=cid).count(), 'TeamNote%sSum.%%s' % title)
#    return McNum(lambda zsite_id: TeamNote.where(zsite_id=zsite_id).count(), 'TeamNoteAllSum.%s')
#
#TEAM_NOTE_TOTAL_DIC = dict((k, _team_note_total_by_cid(k, v)) for k, v in CID_TITLE_TUPLE)
#
#def team_note_total_by_cid(zsite_id, cid):
#    return TEAM_NOTE_TOTAL_DIC[cid](zsite_id)
#
#def mc_flush(zsite_id, cid):
#    mc_flush_cid(zsite_id, cid)
#    mc_flush_cid(zsite_id, CID_ALL)
#
#def mc_flush_cid(zsite_id, cid):
#    TEAM_NOTE_TOTAL_DIC[int(cid)].delete(zsite_id)
#    for order in ORDER_DIC:
#        mc_team_note_id_list.delete('%s_%s_%s' % (zsite_id, cid, order))
