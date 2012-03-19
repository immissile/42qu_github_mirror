#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import cursor_by_table, McModel, McLimitA, McCache, McCacheA, Model, McNum, McCacheM
from txt2htm import RE_AT
from txt import txt_get, txt_new
from zsite_url import id_by_url
from collections import defaultdict
from mq import mq_client
from model.buzz_po_bind_user import buzz_po_bind_user
#def mq_client(f):
#    return f



# buzz_at
# id
# from_id
# to_id
# po_id
# reply_id
# state

#CREATE TABLE `zpage`.`buzz_at` (
#  `id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
#  `from_id` INTEGER UNSIGNED NOT NULL,
#  `to_id` INTEGER UNSIGNED NOT NULL,
#  `reply_id` INTEGER UNSIGNED NOT NULL,
#  `state` TINYINT UNSIGNED NOT NULL DEFAULT 30,
#  `po_id` INTEGER UNSIGNED NOT NULL,
#  PRIMARY KEY (`id`),
#  INDEX `Index_2`(`to_id`, `state`, `id`),
#  INDEX `Index_3`(`po_id`)
#)
#ENGINE = MyISAM;

# buzz_at_pos
# id
# value

BUZZ_AT_SHOW = 30
BUZZ_AT_HIDE = 20
BUZZ_AT_RMED = 0

mc_po_list_by_buzz_at_user_id = McCacheM('BuzzAtByUserIdForShow:%s')

class BuzzAt(Model):
    pass

def at_id_set_by_txt(txt):
    return set(filter(bool, [id_by_url(i[2]) for i in RE_AT.findall(txt)]))

def buzz_at_hide(user_id, po_id=0):
    if po_id:
        BuzzAt.where(po_id=po_id,to_id=user_id).update(state=BUZZ_AT_HIDE)
    else:
        for i in po_list_by_buzz_at_user_id(user_id):
            po_id = i[0]
            BuzzAt.where(po_id=po_id,to_id=user_id).update(state=BUZZ_AT_HIDE)
    mc_flush(user_id)

def buzz_at_new(from_id, txt, po_id, reply_id=0):
    at_id_set = at_id_set_by_txt(txt)
    for to_id in at_id_set:
        buzz_at = BuzzAt(from_id=from_id, to_id=to_id, reply_id=reply_id, po_id=po_id, state=BUZZ_AT_SHOW)
        buzz_at.save()
        mc_flush(to_id)
        mc_po_list_by_buzz_at_user_id.delete(to_id)

    return at_id_set

mq_buzz_at_new = mq_client(buzz_at_new)


def buzz_at_reply_rm(reply_id):
    from model.reply import Reply
    txt = txt_get(reply_id)
    if not txt:
        return
    at_id_set = at_id_set_by_txt(txt)
    for to_id in at_id_set:
        BuzzAt.where(to_id=to_id, reply_id=reply_id).update(state=BUZZ_AT_RMED)
        mc_flush(to_id)

BUZZ_AT_COL = 'id,from_id,po_id,reply_id'


def buzz_at_dump_for_show(li):
    po_id_list = []
    reply_id_list = []
    for id, from_id, po_id, reply_id in li:
        po_id_list.append(po_id)
        if reply_id:
            reply_id_list.append(po_id)

    from model.reply import Reply
    from model.po import Po
    po_mc_get_dict = Po.mc_get_dict(po_id_list)
    result = []
    return result


buzz_at_count = McNum(lambda user_id: BuzzAt.where(to_id=user_id, state=BUZZ_AT_SHOW).count(), 'BuzzAtCount+%s')

def mc_flush(user_id):
    buzz_at_count.delete(user_id)
    mc_po_list_by_buzz_at_user_id.delete(user_id)

def buzz_at_col_list(user_id, limit, offset):
    return BuzzAt.where(
        to_id=user_id
    ).where('state>=%s', BUZZ_AT_HIDE).order_by('id desc').col_list(
        limit, offset, BUZZ_AT_COL
    )

def buzz_at_list(user_id, limit, offset):
    po_id_list = []
    reply_id_list = []
    user_id_list = []
    id_list = []
    for id, from_id, po_id, reply_id in buzz_at_col_list(user_id, limit, offset):
        id_list.append(id)
        po_id_list.append(po_id)
        reply_id_list.append(reply_id)
        user_id_list.append(from_id)

    from model.zsite import Zsite
    from model.po import Po
    from model.reply import Reply
    return tuple(zip(
        id_list,
        Zsite.mc_get_list(user_id_list),
        Po.mc_get_list(po_id_list),
        Reply.mc_get_list(reply_id_list),
    ))

@mc_po_list_by_buzz_at_user_id('{user_id}')
def po_list_by_buzz_at_user_id(user_id):
    from model.po import Po

    result = BuzzAt.where(
        to_id=user_id, state=BUZZ_AT_SHOW
    ).order_by('id desc').col_list(
        32, 0, 'id, from_id, po_id, reply_id'
    )
    id_list = []
    id2user = defaultdict(list)
    for id, from_id, po_id, reply_id in result:
        po_id_in = po_id in id2user
        if po_id_in or len(id_list)<7:
            if not po_id_in:
                id_list.append(po_id) 
            id2user[po_id].append(from_id)
         
    po_list = Po.mc_get_list(id_list)

    return buzz_po_bind_user(po_list, [
        id2user[i.id] for i in po_list
    ])

if __name__ == '__main__':
    pass

    print po_list_by_buzz_at_user_id(10000000)
    class BuzzAtPos(Model):
        pass

    from model.zsite import Zsite, CID_USER
    from zweb.orm import ormiter
    for i in ormiter(BuzzAtPos):
        user_id = i.id
        value = i.value
        if user_id:
            print user_id
            for j in BuzzAt.where(state=BUZZ_AT_SHOW).where('id<=%s'%value).where(to_id=user_id):
                j.state = BUZZ_AT_HIDE
                j.save()



