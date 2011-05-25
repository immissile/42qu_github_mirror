#!/usr/bin/env python
# -*- coding: utf-8 -*-
from reddit_rank import hot, confidence
from _db import Model, McModel, McCache, McCacheA, McLimitA, McNum
from vote import vote_up_count, vote_down_count

class Rank(McModel):
    pass


mc_team_id_by_note_id = McCache("TeamIdByNoteId:%s")

@mc_team_id_by_note_id("{note_id}")
def team_id_by_note_id(note_id):
    t = TeamNote.mc_get(note_id)
    if t:
        return t.team_id
    return 0

def team_by_note_id(note_id):
    id = team_id_by_note_id(note_id)
    if id:
        man = Man.mc_get(id)
        return man

def team_note_new(man_id, team_id, cid, title, txt, repaste=None):
    subject_state = NOTE_SUBJECT_STATE_FAV if repaste else NOTE_SUBJECT_STATE_REVIEW
    subject_id = man_note_subject_id_state(man_id, subject_state).id
    note = note_new(man_id, title, txt, subject_id)
    note_id = note.id

    return _team_note_new(note_id, team_id, cid)

def _team_note_new(note_id, team_id, cid):
    note = Note.mc_get(note_id)

    team_note_fav_new(note_id, team_id)

    t = TeamNote(id=note_id, team_id=team_id, cid=cid)
    up, down = note_rate_tuple(note_id)
    t.hot = hot(up, down, note.create_time)
    t.confidence = confidence(up, down)
    t.save()
    mc_team_id_by_note_id.set(note_id, team_id)
    mc_flush(team_id, cid)
    return t

def team_note_fav_new(note_id, team_id):
    id = feed_entry_new_id(FEED_CID_NOTE_FAV, team_id)
    NoteFav.raw_sql('insert into note_fav (id, man_id, rid, reply_id) values (%s, %s, %s, null)', id, team_id, note_id)

def team_note_mv(note_id, cid):
    n = TeamNote.mc_get(note_id)
    if n:
        o_cid = n.cid
        if o_cid != cid and cid in CID_ID_STR_TUPLE[1:]:
            cid = int(cid)
            n.cid = cid
            n.save()
            team_id = n.team_id
            mc_flush_cid(team_id, o_cid)
            mc_flush_cid(team_id, cid)

def team_note_rm(note_id):
    n = TeamNote.mc_get(note_id)
    if n:
        team_id = n.team_id
        team_note_fav_rm(note_id, team_id)
        n.delete()
        mc_team_id_by_note_id.set(note_id, 0)
        mc_flush(team_id, n.cid)

def team_note_fav_rm(note_id, team_id):
    for i in NoteFav.where(man_id=team_id, rid=note_id):
        feed_entry_rm(i.id)
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
            mc_flush(t.team_id, t.cid)

ID_CACHE_LIMIT = 256

mc_team_note_id_list = McLimitA('TeamNoteIdList.%s', ID_CACHE_LIMIT)

@mc_team_note_id_list('{team_id}_{cid}_{order}')
def team_note_id_list(team_id, cid, order, offset, limit):
    qs = TeamNote.where(team_id=team_id)
    if cid:
        qs = qs.where(cid=cid)
    order = ORDER_DIC[order]
    return qs.order_by('%s desc' % order).id_list(limit, offset)

def team_note_list(team_id, cid, order, offset=0, limit=3):
    ids = team_note_id_list(team_id, cid, order, offset, limit)
    return Note.mc_get_list(ids)

def _team_note_total_by_cid(cid, title):
    if cid:
        return McTotal(lambda team_id: TeamNote.where(team_id=team_id, cid=cid).count(), 'TeamNote%sSum.%%s' % title)
    return McTotal(lambda team_id: TeamNote.where(team_id=team_id).count(), 'TeamNoteAllSum.%s')

TEAM_NOTE_TOTAL_DIC = dict((k, _team_note_total_by_cid(k, v)) for k, v in CID_TITLE_TUPLE)

def team_note_total_by_cid(team_id, cid):
    return TEAM_NOTE_TOTAL_DIC[cid](team_id)

def mc_flush(team_id, cid):
    mc_flush_cid(team_id, cid)
    mc_flush_cid(team_id, CID_ALL)

def mc_flush_cid(team_id, cid):
    TEAM_NOTE_TOTAL_DIC[int(cid)].delete(team_id)
    for order in ORDER_DIC:
        mc_team_note_id_list.delete('%s_%s_%s' % (team_id, cid, order))

if __name__ == '__main__':
    pass
