#!/usr/bin/env python
# -*- coding: utf-8 -*-
from reddit_rank import hot, confidence
from _db import Model, McModel, McCache, McCacheA, McLimitA, McNum
from vote import vote_up_count, vote_down_count
from zsite import Zsite

class Rank(McModel):
    pass

mc_zsite_id_list_by_po_id = McCacheA('ZsiteIdListByPoId:%s')

@mc_zsite_id_list_by_po_id('{po_id}')
def zsite_id_list_by_po_id(po_id):
    return Rank.where(po_id=po_id).field_list(field='rid')

def zsite_list_by_po_id(po_id):
    ids = zsite_id_list_by_po_id(po_id)
    return Zsite.mc_get_list(ids)

#TODO 日记分类tag实现
def team_note_new(man_id, zsite_id, cid, title, txt, repaste=None):
    subject_state = NOTE_SUBJECT_STATE_FAV if repaste else NOTE_SUBJECT_STATE_REVIEW
    subject_id = man_note_subject_id_state(man_id, subject_state).id
    note = note_new(man_id, title, txt, subject_id)
    note_id = note.id

    return _team_note_new(note_id, zsite_id, cid)

def _team_note_new(note_id, zsite_id, cid):
    note = Note.mc_get(note_id)

    team_note_fav_new(note_id, zsite_id)

    t = TeamNote(id=note_id, zsite_id=zsite_id, cid=cid)
    up, down = note_rate_tuple(note_id)
    t.hot = hot(up, down, note.create_time)
    t.confidence = confidence(up, down)
    t.save()
    mc_zsite_id_by_note_id.set(note_id, zsite_id)
    mc_flush(zsite_id, cid)
    return t

def team_note_fav_new(note_id, zsite_id):
    id = feed_new_id(FEED_CID_NOTE_FAV, zsite_id)
    NoteFav.raw_sql('insert into note_fav (id, man_id, rid, reply_id) values (%s, %s, %s, null)', id, zsite_id, note_id)

def team_note_mv(note_id, cid):
    n = TeamNote.mc_get(note_id)
    if n:
        o_cid = n.cid
        if o_cid != cid and cid in CID_ID_STR_TUPLE[1:]:
            cid = int(cid)
            n.cid = cid
            n.save()
            zsite_id = n.zsite_id
            mc_flush_cid(zsite_id, o_cid)
            mc_flush_cid(zsite_id, cid)

def team_note_rm(note_id):
    n = TeamNote.mc_get(note_id)
    if n:
        zsite_id = n.zsite_id
        team_note_fav_rm(note_id, zsite_id)
        n.delete()
        mc_zsite_id_by_note_id.set(note_id, 0)
        mc_flush(zsite_id, n.cid)

def team_note_fav_rm(note_id, zsite_id):
    for i in NoteFav.where(man_id=zsite_id, rid=note_id):
        feed_rm(i.id)
        i.delete()

def team_note_rank(note_id):
    n = Note.mc_get(note_id)
    if n:
        t = TeamNote.mc_get(note_id)
        if t:
            up, down = note_rate_tuple(note_id)
            t.hot = hot(up, down, n.create_time)
            t.confidence = confidence(up, down)
            t.save()
            mc_flush(t.zsite_id, t.cid)

ID_CACHE_LIMIT = 256

mc_team_note_id_list = McLimitA('TeamNoteIdList.%s', ID_CACHE_LIMIT)

@mc_team_note_id_list('{zsite_id}_{cid}_{order}')
def team_note_id_list(zsite_id, cid, order, offset, limit):
    qs = TeamNote.where(zsite_id=zsite_id)
    if cid:
        qs = qs.where(cid=cid)
    order = ORDER_DIC[order]
    return qs.order_by('%s desc' % order).field_list(limit, offset)

def team_note_list(zsite_id, cid, order, offset=0, limit=3):
    ids = team_note_id_list(zsite_id, cid, order, offset, limit)
    return Note.mc_get_list(ids)

def _team_note_total_by_cid(cid, title):
    if cid:
        return McNum(lambda zsite_id: TeamNote.where(zsite_id=zsite_id, cid=cid).count(), 'TeamNote%sSum.%%s' % title)
    return McNum(lambda zsite_id: TeamNote.where(zsite_id=zsite_id).count(), 'TeamNoteAllSum.%s')

TEAM_NOTE_TOTAL_DIC = dict((k, _team_note_total_by_cid(k, v)) for k, v in CID_TITLE_TUPLE)

def team_note_total_by_cid(zsite_id, cid):
    return TEAM_NOTE_TOTAL_DIC[cid](zsite_id)

def mc_flush(zsite_id, cid):
    mc_flush_cid(zsite_id, cid)
    mc_flush_cid(zsite_id, CID_ALL)

def mc_flush_cid(zsite_id, cid):
    TEAM_NOTE_TOTAL_DIC[int(cid)].delete(zsite_id)
    for order in ORDER_DIC:
        mc_team_note_id_list.delete('%s_%s_%s' % (zsite_id, cid, order))

if __name__ == '__main__':
    pass
