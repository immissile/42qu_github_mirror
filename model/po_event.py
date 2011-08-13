#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import McCache, McNum
from cid import CID_EVENT
from po import Po, po_new, po_word_new, po_note_new, po_rm, po_cid_set
from state import STATE_DEL, STATE_SECRET, STATE_ACTIVE
from txt import txt_new, txt_get
from zkit.time_format import time_title
from zsite import Zsite
from model.cid import CID_EVENT, CID_EVENT_FEEDBACK
from model.pic import pic_new_save , fs_url_jpg , fs_set_jpg
from zkit.pic import pic_fit
from rank import rank_po_id_list
from event import EVENT_CID, EVENT_CID_CN, EventJoiner

mc_event_feedback_id_get = McCache('EventFeedBackGet.%s')

@mc_event_feedback_id_get("{user_id}_{event_id}")
def event_feedback_id_get(user_id, event_id):
    for i in Po.where(user_id=user_id, rid=event_id).where(
        cid = CID_EVENT_FEEDBACK
    ).where('state>%s', STATE_DEL).col_list(1, 0):
        return i
    return 0

event_feedback_count = McNum(
    lambda event_id, state: EventJoiner.where(
        event_id=event_id, state=state
    ).count(), 'EventFeedbackCount:%s'
)

def po_event_pic_new(zsite_id, pic):
    pic_id = pic_new_save(CID_EVENT, zsite_id, pic)
    pic162 = pic_fit(pic, 162)
    fs_set_jpg(162, pic_id, pic162)
    return pic_id


def po_event_feedback_new(user_id, name, txt, event_id, event_user_id):
    if not name and not txt:
        return

    id = event_feedback_id_get(user_id, event_id)

    if id:
        return Po.mc_get(id)
    else:
        m = po_new(CID_EVENT_FEEDBACK, user_id, name, STATE_ACTIVE, event_id)
        id = m.id
        mc_event_feedback_id_get.set('%s_%s' % (user_id, event_id), id)
        m.feed_new()

        from buzz import buzz_event_feedback_new , mq_buzz_event_feedback_owner_new
        
        if user_id!=event_user_id:
            rank_new(m, event_id, CID_EVENT_FEEDBACK)
            buzz_event_feedback_new(user_id, id)
        else:
            mq_buzz_event_feedback_owner_new(user_id, id)

def po_event_feedback_rm(user_id, event_id):
    event_joiner = event_joiner_get(event_id, user_id)
    state = event_joiner.state
    event_joiner.state = EVENT_JOIN_STATE_END
    event_joiner.save()
    event_feedback_count.delete('%s_%s'%(event_id, state))

#event_feedback_count


def po_event_feedback_list(event_id, zsite_id=0, user_id=0):
    ids = rank_po_id_list(event_id, CID_EVENT_FEEDBACK, 'confidence')
    print 'ids:', ids
    if zsite_id == user_id:
        zsite_id = 0
    
    user_ids = filter(bool, (zsite_id, user_id))
    if user_ids:
        _ids = []
        for i in user_ids:
            user_feedback_id = event_feedback_id_get(i, event_id)
            if user_feedback_id:
                _ids.append(user_feedback_id)
                if user_feedback_id in ids:
                    ids.remove(user_feedback_id)
        if _ids:
            _ids.extend(ids)
            ids = _ids

    li = Po.mc_get_list(ids)
    Zsite.mc_bind(li, 'user', 'user_id')
    return li


if __name__ == '__main__':
    print EVENT_CID







